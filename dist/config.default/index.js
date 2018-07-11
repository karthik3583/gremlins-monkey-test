'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});

var _browser = require('./browser');

var _browser2 = _interopRequireDefault(_browser);

var _gremlins = require('./gremlins');

var _gremlins2 = _interopRequireDefault(_gremlins);

var _page = require('./page');

var _page2 = _interopRequireDefault(_page);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

exports.default = {
  browser: _browser2.default,
  gremlins: _gremlins2.default,
  page: _page2.default
};