from models import *


class SQLProviderRegulator:
    @staticmethod
    def get_regulator_modes():
        """
        Get setted regulator modes
        """
        states = RegulationMode.query\
        .join(
            Regulator, RegulationMode.regulator_id == Regulator.id
        )\
        .join(
            Link, RegulationMode.regulator_id == Link.regulator_id
        )\
        .where(
            Link.status == True
        )\
        .group_by(
            Link.regulator_id
        )\
        .order_by(
            func.max(RegulationMode.timestamp).desc()
        )\
        .add_columns(
            Link.regulator_id,
            Regulator.name,
            Regulator.gpio,
            RegulationMode.required,
            RegulationMode.timestamp
        )\
        .all()
        return states


    @staticmethod
    def get_linked_regulators():
        states = Regulator.query\
        .join(
            Link, Regulator.id == Link.regulator_id
        )\
        .where(Link.status == True)\
        .all()

        return states
