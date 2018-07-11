'use strict';

require('babel-polyfill');

var _yargs = require('yargs');

var _yargs2 = _interopRequireDefault(_yargs);

var _getConfig = require('./lib/getConfig');

var _getConfig2 = _interopRequireDefault(_getConfig);

var _gremlinsPuppet = require('./lib/gremlinsPuppet');

var _gremlinsPuppet2 = _interopRequireDefault(_gremlinsPuppet);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _asyncToGenerator(fn) { return function () { var gen = fn.apply(this, arguments); return new Promise(function (resolve, reject) { function step(key, arg) { try { var info = gen[key](arg); var value = info.value; } catch (error) { reject(error); return; } if (info.done) { resolve(value); } else { return Promise.resolve(value).then(function (value) { step("next", value); }, function (err) { step("throw", err); }); } } return step("next"); }); }; }

var init = function () {
  var _ref = _asyncToGenerator( /*#__PURE__*/regeneratorRuntime.mark(function _callee() {
    var config, argv;
    return regeneratorRuntime.wrap(function _callee$(_context) {
      while (1) {
        switch (_context.prev = _context.next) {
          case 0:
            config = (0, _getConfig2.default)();
            argv = _yargs2.default.usage('$0 -url [url]').default('url', config.page.entryPoint).demandOption(['url']).argv;

            (0, _gremlinsPuppet2.default)(argv.url, config);

          case 3:
          case 'end':
            return _context.stop();
        }
      }
    }, _callee, undefined);
  }));

  return function init() {
    return _ref.apply(this, arguments);
  };
}();

init();