'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});

function _asyncToGenerator(fn) { return function () { var gen = fn.apply(this, arguments); return new Promise(function (resolve, reject) { function step(key, arg) { try { var info = gen[key](arg); var value = info.value; } catch (error) { reject(error); return; } if (info.done) { resolve(value); } else { return Promise.resolve(value).then(function (value) { step("next", value); }, function (err) { step("throw", err); }); } } return step("next"); }); }; }

var WAIT_TIME = 750;

var getCurrentUrl = function getCurrentUrl(_targetInfo) {
  return _targetInfo.url.split('?')[0];
};

var handleTimeout = function handleTimeout(page, urls, timeout) {
  return setTimeout(_asyncToGenerator( /*#__PURE__*/regeneratorRuntime.mark(function _callee() {
    var target, timestamp;
    return regeneratorRuntime.wrap(function _callee$(_context) {
      while (1) {
        switch (_context.prev = _context.next) {
          case 0:
            target = urls[Math.floor(Math.random() * urls.length)];
            timestamp = Date.now();
            _context.next = 4;
            return page.goto(target === currentUrl ? target + '?t=' + timestamp : target, {
              waitUntil: 'networkidle2'
            });

          case 4:
          case 'end':
            return _context.stop();
        }
      }
    }, _callee, undefined);
  })), timeout);
};

var buildTimeout = function buildTimeout(time) {
  var instance = null;
  return {
    clear: function clear() {
      if (instance) {
        clearTimeout(instance);
      }
    },
    set: function set(handleFunction) {
      instance = setTimeout(handleFunction, time);
    }
  };
};

var buildHandleTimeout = function buildHandleTimeout(page, urls, currentUrl) {
  return _asyncToGenerator( /*#__PURE__*/regeneratorRuntime.mark(function _callee2() {
    var target, timestamp;
    return regeneratorRuntime.wrap(function _callee2$(_context2) {
      while (1) {
        switch (_context2.prev = _context2.next) {
          case 0:
            target = urls[Math.floor(Math.random() * urls.length)];
            timestamp = Date.now();
            _context2.next = 4;
            return page.goto(target === currentUrl ? target + '?t=' + timestamp : target, {
              waitUntil: 'networkidle2'
            });

          case 4:
          case 'end':
            return _context2.stop();
        }
      }
    }, _callee2, undefined);
  }));
};

exports.default = function (config, page) {
  var timeout = buildTimeout(config.gremlins.timeout);
  var urls = [];
  return function () {
    var _ref4 = _asyncToGenerator( /*#__PURE__*/regeneratorRuntime.mark(function _callee3(_ref3) {
      var _targetInfo = _ref3._targetInfo;
      var currentUrl, handleTimeout;
      return regeneratorRuntime.wrap(function _callee3$(_context3) {
        while (1) {
          switch (_context3.prev = _context3.next) {
            case 0:
              currentUrl = getCurrentUrl(_targetInfo);

              urls.push(_targetInfo.url);
              timeout.clear();
              _context3.next = 5;
              return page.waitFor(WAIT_TIME);

            case 5:
              _context3.next = 7;
              return page.addScriptTag({ path: './lib/gremlinsClient.js' });

            case 7:
              handleTimeout = buildHandleTimeout(page, urls, currentUrl);

              timeout.set(handleTimeout);

            case 9:
            case 'end':
              return _context3.stop();
          }
        }
      }, _callee3, undefined);
    }));

    return function (_x) {
      return _ref4.apply(this, arguments);
    };
  }();
};