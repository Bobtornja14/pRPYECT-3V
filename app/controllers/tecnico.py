from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models.models import Asignacion, Reporte, Parte, PedidoPieza, Tecnico
from app.forms import ReporteForm, PedidoPiezaForm
from app.decorators import tecnico_required
from datetime import datetime
import json

tecnico_bp = Blueprint('tecnico', __name__)


def get_tecnico_for_user(user):
    """Obtiene el perfil de técnico para un usuario"""
    # Primero buscar por usuario_id
    tecnico = Tecnico.query.filter_by(usuario_id=user.id).first()

    # Si no se encuentra, buscar por email como fallback
    if not tecnico and user.email:
        tecnico = Tecnico.query.filter_by(email=user.email).first()

        # Si se encuentra por email, asociar con el usuario
        if tecnico:
            tecnico.usuario_id = user.id
            db.session.commit()

    return tecnico


@tecnico_bp.route('/dashboard')
@tecnico_required
def dashboard():
    tecnico = get_tecnico_for_user(current_user)

    if not tecnico:
        flash('No se encontró perfil de técnico asociado. Contacte al administrador.', 'error')
        return redirect(url_for('auth.logout'))

    # Estadísticas del técnico
    asignaciones_pendientes = Asignacion.query.filter_by(tecnico_id=tecnico.id, estado='asignada').count()
    asignaciones_proceso = Asignacion.query.filter_by(tecnico_id=tecnico.id, estado='en_proceso').count()
    asignaciones_completadas = Asignacion.query.filter_by(tecnico_id=tecnico.id, estado='completada').count()

    # Pedidos de piezas pendientes
    pedidos_pendientes = PedidoPieza.query.filter_by(tecnico_id=tecnico.id, estado='pendiente').count()

    # Últimas asignaciones
    ultimas_asignaciones = Asignacion.query.filter_by(tecnico_id=tecnico.id) \
        .order_by(Asignacion.fecha_asignacion.desc()) \
        .limit(5).all()

    return render_template('tecnico/dashboard.html',
                           asignaciones_pendientes=asignaciones_pendientes,
                           asignaciones_proceso=asignaciones_proceso,
                           asignaciones_completadas=asignaciones_completadas,
                           pedidos_pendientes=pedidos_pendientes,
                           ultimas_asignaciones=ultimas_asignaciones,
                           tecnico=tecnico)


@tecnico_bp.route('/asignaciones')
@tecnico_required
def mis_asignaciones():
    tecnico = get_tecnico_for_user(current_user)

    if not tecnico:
        flash('No se encontró perfil de técnico asociado', 'error')
        return redirect(url_for('main.index'))

    page = request.args.get('page', 1, type=int)
    estado = request.args.get('estado', 'todas')

    query = Asignacion.query.filter_by(tecnico_id=tecnico.id)

    if estado == 'pendientes':
        query = query.filter_by(estado='asignada')
    elif estado == 'proceso':
        query = query.filter_by(estado='en_proceso')
    elif estado == 'completadas':
        query = query.filter_by(estado='completada')

    asignaciones = query.order_by(Asignacion.fecha_asignacion.desc()).paginate(
        page=page, per_page=10, error_out=False)

    return render_template('tecnico/asignaciones.html',
                           asignaciones=asignaciones,
                           estado_actual=estado)


@tecnico_bp.route('/asignacion/<int:id>/iniciar', methods=['POST'])
@tecnico_required
def iniciar_asignacion(id):
    tecnico = get_tecnico_for_user(current_user)
    if not tecnico:
        flash('No se encontró perfil de técnico', 'error')
        return redirect(url_for('tecnico.dashboard'))

    asignacion = Asignacion.query.filter_by(id=id, tecnico_id=tecnico.id).first_or_404()

    if asignacion.estado == 'asignada':
        asignacion.estado = 'en_proceso'
        asignacion.fecha_inicio = datetime.utcnow()
        db.session.commit()
        flash('Asignación iniciada exitosamente', 'success')

    return redirect(url_for('tecnico.mis_asignaciones'))


@tecnico_bp.route('/reporte/<int:asignacion_id>', methods=['GET', 'POST'])
@tecnico_required
def crear_reporte(asignacion_id):
    tecnico = get_tecnico_for_user(current_user)
    if not tecnico:
        flash('No se encontró perfil de técnico', 'error')
        return redirect(url_for('tecnico.dashboard'))

    asignacion = Asignacion.query.filter_by(id=asignacion_id, tecnico_id=tecnico.id).first_or_404()

    # Verificar si ya existe un reporte
    reporte_existente = Reporte.query.filter_by(asignacion_id=asignacion_id).first()

    form = ReporteForm()

    if reporte_existente:
        # Cargar datos existentes
        if request.method == 'GET':
            form.trabajo_realizado.data = reporte_existente.trabajo_realizado
            form.problemas_encontrados.data = reporte_existente.problemas_encontrados
            form.solucion_aplicada.data = reporte_existente.solucion_aplicada
            form.recomendaciones.data = reporte_existente.recomendaciones
            form.estado_inicial.data = reporte_existente.estado_inicial
            form.estado_final.data = reporte_existente.estado_final
            form.cliente_satisfecho.data = reporte_existente.cliente_satisfecho
            form.observaciones_cliente.data = reporte_existente.observaciones_cliente

            if reporte_existente.hora_inicio:
                form.hora_inicio.data = reporte_existente.hora_inicio.strftime('%H:%M')
            if reporte_existente.hora_fin:
                form.hora_fin.data = reporte_existente.hora_fin.strftime('%H:%M')

    if form.validate_on_submit():
        if reporte_existente:
            reporte = reporte_existente
        else:
            reporte = Reporte(
                asignacion_id=asignacion_id,
                tecnico_id=tecnico.id
            )

        # Actualizar datos del reporte
        reporte.trabajo_realizado = form.trabajo_realizado.data
        reporte.problemas_encontrados = form.problemas_encontrados.data
        reporte.solucion_aplicada = form.solucion_aplicada.data
        reporte.recomendaciones = form.recomendaciones.data
        reporte.estado_inicial = form.estado_inicial.data
        reporte.estado_final = form.estado_final.data
        reporte.cliente_satisfecho = form.cliente_satisfecho.data
        reporte.observaciones_cliente = form.observaciones_cliente.data

        # Procesar horas
        try:
            if form.hora_inicio.data:
                hora_inicio = datetime.strptime(form.hora_inicio.data, '%H:%M').time()
                reporte.hora_inicio = datetime.combine(datetime.now().date(), hora_inicio)

            if form.hora_fin.data:
                hora_fin = datetime.strptime(form.hora_fin.data, '%H:%M').time()
                reporte.hora_fin = datetime.combine(datetime.now().date(), hora_fin)

            # Calcular tiempo total
            if reporte.hora_inicio and reporte.hora_fin:
                delta = reporte.hora_fin - reporte.hora_inicio
                reporte.tiempo_total = int(delta.total_seconds() / 60)  # en minutos
        except ValueError:
            flash('Formato de hora inválido. Use HH:MM', 'error')
            return render_template('tecnico/reporte_form.html', form=form, asignacion=asignacion)

        if not reporte_existente:
            db.session.add(reporte)

        db.session.commit()
        flash('Reporte guardado exitosamente', 'success')
        return redirect(url_for('tecnico.ver_reporte', asignacion_id=asignacion_id))

    return render_template('tecnico/reporte_form.html', form=form, asignacion=asignacion)


@tecnico_bp.route('/reporte/<int:asignacion_id>/ver')
@tecnico_required
def ver_reporte(asignacion_id):
    tecnico = get_tecnico_for_user(current_user)
    if not tecnico:
        flash('No se encontró perfil de técnico', 'error')
        return redirect(url_for('tecnico.dashboard'))

    asignacion = Asignacion.query.filter_by(id=asignacion_id, tecnico_id=tecnico.id).first_or_404()
    reporte = Reporte.query.filter_by(asignacion_id=asignacion_id).first()

    return render_template('tecnico/reporte_ver.html', asignacion=asignacion, reporte=reporte)


@tecnico_bp.route('/reporte/<int:asignacion_id>/firmar', methods=['POST'])
@tecnico_required
def guardar_firma(asignacion_id):
    tecnico = get_tecnico_for_user(current_user)
    if not tecnico:
        return jsonify({'success': False, 'message': 'No se encontró perfil de técnico'})

    asignacion = Asignacion.query.filter_by(id=asignacion_id, tecnico_id=tecnico.id).first_or_404()
    reporte = Reporte.query.filter_by(asignacion_id=asignacion_id).first_or_404()

    data = request.get_json()
    firma_data = data.get('firma')
    nombre_cliente = data.get('nombre_cliente', '')

    if firma_data:
        # Limpiar el prefijo data:image/png;base64,
        if firma_data.startswith('data:image/png;base64,'):
            firma_data = firma_data.replace('data:image/png;base64,', '')

        reporte.firma_cliente = firma_data
        reporte.nombre_firma = nombre_cliente
        reporte.completado = True

        # Marcar asignación como completada
        asignacion.estado = 'completada'
        asignacion.fecha_finalizacion = datetime.utcnow()

        db.session.commit()

        return jsonify({'success': True, 'message': 'Firma guardada exitosamente'})

    return jsonify({'success': False, 'message': 'Error al guardar la firma'})


@tecnico_bp.route('/inventario')
@tecnico_required
def ver_inventario():
    page = request.args.get('page', 1, type=int)
    buscar = request.args.get('buscar', '')

    query = Parte.query.filter_by(activo=True)

    if buscar:
        query = query.filter(
            db.or_(
                Parte.nombre.contains(buscar),
                Parte.codigo.contains(buscar),
                Parte.descripcion.contains(buscar)
            )
        )

    partes = query.order_by(Parte.nombre).paginate(
        page=page, per_page=15, error_out=False)

    return render_template('tecnico/inventario.html', partes=partes, buscar=buscar)


@tecnico_bp.route('/pedido-pieza', methods=['GET', 'POST'])
@tecnico_required
def solicitar_pieza():
    tecnico = get_tecnico_for_user(current_user)
    if not tecnico:
        flash('No se encontró perfil de técnico', 'error')
        return redirect(url_for('tecnico.dashboard'))

    form = PedidoPiezaForm()

    # Cargar opciones de piezas activas
    form.parte_id.choices = [(p.id, f"{p.codigo} - {p.nombre} (Stock: {p.stock})")
                             for p in Parte.query.filter_by(activo=True).all()]

    if form.validate_on_submit():
        pedido = PedidoPieza(
            tecnico_id=tecnico.id,
            parte_id=form.parte_id.data,
            cantidad_solicitada=form.cantidad_solicitada.data,
            motivo=form.motivo.data,
            urgencia=form.urgencia.data,
            estado='pendiente',  # <-- Asegura que el estado sea 'pendiente'
            asignacion_id=form.asignacion_id.data if hasattr(form, 'asignacion_id') and form.asignacion_id.data else None
        )

        db.session.add(pedido)
        db.session.commit()
        flash('Pedido de pieza enviado exitosamente', 'success')
        return redirect(url_for('tecnico.mis_pedidos'))

    return render_template('tecnico/pedido_form.html', form=form)


@tecnico_bp.route('/mis-pedidos')
@tecnico_required
def mis_pedidos():
    tecnico = get_tecnico_for_user(current_user)
    if not tecnico:
        flash('No se encontró perfil de técnico', 'error')
        return redirect(url_for('tecnico.dashboard'))

    page = request.args.get('page', 1, type=int)
    estado = request.args.get('estado', 'todos')

    query = PedidoPieza.query.filter_by(tecnico_id=tecnico.id)

    if estado == 'pendientes':
        query = query.filter_by(estado='pendiente')
    elif estado == 'aprobados':
        query = query.filter_by(estado='aprobado')
    elif estado == 'entregados':
        query = query.filter_by(estado='entregado')
    elif estado == 'rechazados':
        query = query.filter_by(estado='rechazado')

    pedidos = query.order_by(PedidoPieza.fecha_pedido.desc()).paginate(
        page=page, per_page=10, error_out=False)

    return render_template('tecnico/mis_pedidos.html', pedidos=pedidos, estado_actual=estado)
