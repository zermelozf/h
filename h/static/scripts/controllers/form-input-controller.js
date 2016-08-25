'use strict';

var Controller = require('../base/controller');
var { setElementState } = require('../util/dom');

/**
 * Controller for form input fields.
 */
class FormInputController extends Controller {
  constructor(element, options) {
    super(element, options);

    this.refs.formInput.addEventListener('focus', () => {
      this.trigger('form-input:focus');
    });

    var inputType = this.refs.formInput.type;

    this.on('change', () => {
      this.trigger('form-input:input', {type: inputType});
    });

    this.on('input', () => {
      // Some but not all browsers deliver an `input` event for checkboxes. Ignore
      // these and just emit when the `change` event occurs.
      if (inputType === 'checkbox' || inputType === 'radio') {
        return;
      }
      this.trigger('form-input:input', {type: inputType});
    });
  }

  update(state) {
    setElementState(this.element, {editing: state.editing});
  }

  focus() {
    this.refs.formInput.focus();
  }

  type() {
    return this.refs.formInput.type;
  }
}

module.exports = FormInputController;
