import sqlalchemy as sa
from ringo.model.modul import ActionItem
from ringo.model.mixins import StateMixin
from ringo.model.statemachine import Statemachine, State, null_handler, null_condition


class TrashbinState(Statemachine):

    def setup(self):
        s1 = State(self, 1, "Editable", disabled_actions={"user": ["delete", "restore"]})
        s2 = State(self, 2, "Trashed", disabled_actions={"user": ["trash", "update", "export", "import"]})

        s1.add_transition(s2, "Delete Item", null_handler, null_condition)
        s2.add_transition(s1, "Restore Item", null_handler, null_condition)
        return s1


class TwoStepDelete(StateMixin):

    """Mixin to change the the workflow how to delete items in two
    steps. Using this Mixim will add two new actions named `erease` and
    `restore`. The origin method `delete` will be changed in the way
    that items will only be marked for deletion. This is similar to put
    the item into a trashcan in the first step. From there the user can
    decide to finally erease the item or restore it."""

    # Attach the statemachines to an internal dictionary
    _statemachines = {'trash_state_id': TrashbinState}

    # Configue a field in the model which saves the current
    # state per state machine
    trash_state_id = sa.Column(sa.Integer, default=1)

    @classmethod
    def get_mixin_actions(cls):
        """Returns a list of actions specific for the mixin.

        :returns: List of ActionItems
        """
        actions = []
        actions.append(ActionItem(name=("Trash"),
                                  url="trash/{id}",
                                  icon="icon-trash",
                                  display="hide-overview",
                                  description="Move item into trash"))
        actions.append(ActionItem(name=("Restore"),
                                  url="restore/{id}",
                                  icon="fa fa-recycle",
                                  display="hide-overview",
                                  description="Restore deleted item"))
        return actions

    # Optional. Create a property to access the statemachine
    # like an attribute. This gets usefull if you want to access
    # the state in overview lists.
    @property
    def trash_state(self):
        state = self.get_statemachine('trash_state_id')
        return state.get_state()
