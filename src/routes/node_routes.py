from flask import Blueprint, jsonify
from src.node_configuration_database import NodeConfigurationDatabase

node_bp = Blueprint('node_routes', __name__)

@node_bp.route('/nodes', methods=['GET'])
def list_nodes():
    try:
        db = NodeConfigurationDatabase()
        nodes = db.list_nodes()
        return jsonify({"success": True, "nodes": nodes})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

