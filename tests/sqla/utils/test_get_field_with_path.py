from python_plugins.sqla.utils.attr import get_field_with_path
from ..models.relations import TrainModel1, TrainModel2, TrainModel3
from ..models.associationproxy import AssociationProxyParent,AssociationProxyChild


def test_get_field_with_path():
    attr, path = get_field_with_path(TrainModel2, "model1.name")
    assert attr == TrainModel1.name
    assert path == [TrainModel2.model1]

    attr, path = get_field_with_path(TrainModel3, "model2.name")
    assert attr == TrainModel2.name
    assert path == [TrainModel3.model2]

    attr, path = get_field_with_path(TrainModel3, "model2.model1.name")
    assert attr == TrainModel1.name
    assert path == [TrainModel3.model2, TrainModel2.model1]

    attr, path = get_field_with_path(AssociationProxyParent, "childrennames")
    assert attr == AssociationProxyChild.name
    assert path == [AssociationProxyParent.children]