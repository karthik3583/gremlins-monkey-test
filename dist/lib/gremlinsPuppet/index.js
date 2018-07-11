'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});

var _buildEnvironment = require('./buildEnvironment');

var _buildEnvironment2 = _interopRequireDefault(_buildEnvironment);

var _createUrlChangeHandler = require('./createUrlChangeHandler');

var _createUrlChangeHandler2 = _interopRequireDefault(_createUrlChangeHandler);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _asyncToGenerator(fn) { return function () { var gen = fn.apply(this, arguments); return new Promise(function (resolve, reject) { function step(key, arg) { try { var info = gen[key](arg); var value = info.value; } catch (error) { reject(error); return; } if (info.done) { resolve(value); } else { return Promise.resolve(value).then(function (value) { step("next", value); }, function (err) { step("throw", err); }); } } return step("next"); }); }; }

var gremlinsPuppet = function () {
  var _ref = _asyncToGenerator( /*#__PURE__*/regeneratorRuntime.mark(function _callee(url, config) {
    var _ref2, browser, page, handleUrlChange;

    return regeneratorRuntime.wrap(function _callee$(_context) {
      while (1) {
        switch (_context.prev = _context.next) {
          case 0:
            _context.next = 2;
            return (0, _buildEnvironment2.default)(config.browser);

          case 2:
            _ref2 = _context.sent;
            browser = _ref2.browser;
            page = _ref2.page;
            handleUrlChange = (0, _createUrlChangeHandler2.default)(config, page);

            browser.on('targetchanged', handleUrlChange);
            _context.next = 9;
            return page.setViewport(config.page.viewport);

          case 9:
            _context.next = 11;
            return page.goto(url, {
              waitUntil: 'networkidle2'
            });

          case 11:
          case 'end':
            return _context.stop();
        }
      }
    }, _callee, undefined);
  }));

  return function gremlinsPuppet(_x, _x2) {
    return _ref.apply(this, arguments);
  };
}();

exports.default = gremlinsPuppet;