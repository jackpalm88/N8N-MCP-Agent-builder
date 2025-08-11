"""
node_configuration_database.py

Šis modulis pārvalda n8n mezglu definīciju ielādi un nodrošina vienkāršu
vaicājumu slāni MCP aģentam. Tas izmanto jau inicializēto `db` objektu no
`main.py`, tāpēc __nedublē__ SQLAlchemy instanci.
"""

from __future__ import annotations

import json
import logging
import os
from typing import Any, Dict, List, Optional

from src.extensions import db  # jau inicializētais Flask‑SQLAlchemy objekts

# ────────────────────────────────────────────────────────────────────────────────
#  SQLAlchemy modeļi
# ────────────────────────────────────────────────────────────────────────────────

class NodeDefinition(db.Model):
    """SQL tabula ar izej­definīcijām, kas noder validācijai & autokompletei."""

    __tablename__ = "node_definitions"

    id = db.Column(db.Integer, primary_key=True)
    node_id = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    display_name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(128))
    subcategory = db.Column(db.String(128))
    icon = db.Column(db.String(256))
    version = db.Column(db.String(32))
    json_data = db.Column(db.Text, nullable=False)  # pilnais .json — noder preview

    # — helpers —
    def to_dict(self) -> Dict[str, Any]:
        return {
            "node_id": self.node_id,
            "name": self.name,
            "display_name": self.display_name,
            "description": self.description,
            "category": self.category,
            "subcategory": self.subcategory,
            "icon": self.icon,
            "version": self.version,
        }


# ────────────────────────────────────────────────────────────────────────────────
#  Galvenā API klase
# ────────────────────────────────────────────────────────────────────────────────

class NodeConfigurationDatabase:  # ← LABOJUMS: nosaukums mainīts no NodeConfigurationDB
    """Augsta līmeņa apvalks: ielāde, vaicājumi, validācijas palīg‑metodes."""

    def __init__(self, logger: Optional[logging.Logger] = None) -> None:
        self.log = logger or logging.getLogger(__name__)

    # ── Ielāde ────────────────────────────────────────────────────────────────

    def _upsert_single(self, data: Dict[str, Any]) -> bool:
        """Ievieto vai atjaunina vienu mezglu; atgriež *True*, ja ielāde veiksmīga."""

        node_id: str | None = data.get("name") or data.get("node_id")
        if not node_id:
            return False  # ─ nav pamata identifikatora

        instance: NodeDefinition | None = NodeDefinition.query.filter_by(node_id=node_id).first()
        if instance is None:
            instance = NodeDefinition(node_id=node_id)
            db.session.add(instance)

        # — pamata laukiem ņem drošāko pieejamo vērtību —
        instance.name = data.get("name", node_id)
        instance.display_name = data.get("displayName", instance.name.title())
        instance.description = data.get("description", "")

        group_val = data.get("group", [])
        if isinstance(group_val, list):
            instance.category = group_val[0] if group_val else ""
        else:
            instance.category = str(group_val)

        instance.subcategory = str(data.get("subcategory", ""))
        instance.icon = data.get("icon", "")
        instance.version = str(data.get("version", 1))
        instance.json_data = json.dumps(data, ensure_ascii=False)
        return True

    def load_from_folder(self, folder: str) -> tuple[int, int]:
        """Rekursīvi lasa visus *.json failus mapē, ignorējot bojātos.

        Atgriež (inserted_count, skipped_count).
        """
        inserted = skipped = 0
        for root, _dirs, files in os.walk(folder):
            for fname in files:
                if not fname.endswith(".json"):
                    continue
                fpath = os.path.join(root, fname)
                try:
                    with open(fpath, "r", encoding="utf-8") as fh:
                        parsed = json.load(fh)
                except Exception as exc:  # noqa: BLE001
                    self.log.warning("[node‑loader] Nelasāms %s → %s", fpath, exc)
                    skipped += 1
                    continue

                # Ignorē sarakstus (dažos failos ir iekšējie resursi, nevis mezgli)
                if isinstance(parsed, list):
                    skipped += 1
                    continue

                if self._upsert_single(parsed):
                    inserted += 1
                else:
                    skipped += 1

        db.session.commit()
        self.log.info("[node‑loader] Ielādēti %s mezgli, izlaisti %s faili", inserted, skipped)
        return inserted, skipped

    # ── Vaicājumi ──────────────────────────────────────────────────────────────

    def list_nodes(self, limit: int = 250) -> List[Dict[str, Any]]:
        """Atgriež līdz *limit* mezgliem kā dict sarakstu."""
        return [n.to_dict() for n in NodeDefinition.query.limit(limit).all()]

    def find_by_name(self, text: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Vienkāršs LIKE %%text%% meklējums pēc name/display_name."""
        pattern = f"%{text}%"
        q = NodeDefinition.query.filter(
            db.or_(NodeDefinition.name.ilike(pattern), NodeDefinition.display_name.ilike(pattern))
        ).limit(limit)
        return [n.to_dict() for n in q]

    def get(self, node_id: str) -> Optional[Dict[str, Any]]:
        n = NodeDefinition.query.filter_by(node_id=node_id).first()
        return n.to_dict() if n else None


# ────────────────────────────────────────────────────────────────────────────────
#  CLI ielādes palaišanai (piem., `python -m src.node_configuration_database`)
# ────────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Ielādē n8n mezglu definīcijas datubāzē.")
    parser.add_argument(
        "folder",
        nargs="?",
        default="database/n8n/packages/nodes-base/nodes",
        help="Saknes mape ar *.json mezglu failiēm",
    )
    args = parser.parse_args()

    loader = NodeConfigurationDatabase()  # ← LABOJUMS: mainīts klases nosaukums
    with db.app.app_context():
        inserted, skipped = loader.load_from_folder(args.folder)
        print(f"Pabeigts: ielādēti {inserted}, izlaisti {skipped}")
