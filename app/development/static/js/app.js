
(function(global) {
"use strict";

// --- dependency modules ----------------------------------
// --- define / local variables ----------------------------
var _runOnNode = "process" in global;
var _runOnWorker = "WorkerLocation" in global;
var _runOnBrowser = "document" in global;

// --- class / interfaces ----------------------------------
function MyClass() {
}

MyClass["prototype"] = {
  "method": MyClass_method
};

// --- implements ------------------------------------------
function MyClass_method(name) { 
}

// --- exports ---------------------------------------------
module["exports"] = MyClass;
global["MyClass" in global ? "MyClass_" : "MyClass"] = MyClass;

})((this || 0).self || global);
