'use strict';

var scrollIntoView = require('scroll-into-view');

var Controller = require('../base/controller');
var setElementState = require('../util/dom').setElementState;

class SearchBucketController extends Controller {
  constructor(element, options) {
    super(element, options);

    this.scrollTo = this.options.scrollTo || scrollIntoView;

    this.refs.header.addEventListener('click', () => {
      this.setState({expanded: !this.state.expanded});
    });

    var timeout = this.options.envFlags && this.options.envFlags.get('timeout');

    this.setState({
      expanded: !!timeout,
    });
  }

  update(state, prevState) {
    setElementState(this.refs.content, {hidden: !state.expanded});
    setElementState(this.element, {expanded: state.expanded});

    // Scroll to element when expanded, except on initial load
    if (typeof prevState.expanded !== 'undefined' && state.expanded) {
      this.scrollTo(this.element);
    }
  }
}

module.exports = SearchBucketController;
