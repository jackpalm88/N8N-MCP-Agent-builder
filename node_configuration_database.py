import os
import json
from main import app, db  # ← izmantot esošos objektus
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Text

class NodeDefinition(db.Model):
    __tablename__ = 'node_definitions'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    type = Column(String(255), nullable=False)
    category = Column(String(255))
    description = Column(Text)
    json_data = Column(Text, nullable=False)

    def __repr__(self):
        return f"<NodeDefinition {self.name}>"

def load_node_definitions(base_dir="database/n8n/packages/nodes-base/nodes"):
    loaded_count = 0
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".json"):
                try:
                    with open(os.path.join(root, file), encoding="utf-8") as f:
                        data = json.load(f)
                        name = data.get("displayName", file.replace(".json", ""))
                        type_ = data.get("name", "")
                        category = data.get("group", [""])[0]
                        description = data.get("description", "")

                        existing = NodeDefinition.query.filter_by(name=name).first()
                        if not existing:
                            node = NodeDefinition(
                                name=name,
                                type=type_,
                                category=category,
                                description=description,
                                json_data=json.dumps(data)
                            )
                            db.session.add(node)
                            loaded_count += 1
                except Exception as e:
                    print(f"Kļūda failā {file}: {e}")
    db.session.commit()
    print(f"Ielādēti {loaded_count} jauni mezgli")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        load_node_definitions()

