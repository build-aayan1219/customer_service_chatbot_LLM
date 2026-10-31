(function(){const e=document.createElement("link").relList;if(e&&e.supports&&e.supports("modulepreload"))return;for(const l of document.querySelectorAll('link[rel="modulepreload"]'))o(l);new MutationObserver(l=>{for(const c of l)if(c.type==="childList")for(const h of c.addedNodes)h.tagName==="LINK"&&h.rel==="modulepreload"&&o(h)}).observe(document,{childList:!0,subtree:!0});function r(l){const c={};return l.integrity&&(c.integrity=l.integrity),l.referrerPolicy&&(c.referrerPolicy=l.referrerPolicy),l.crossOrigin==="use-credentials"?c.credentials="include":l.crossOrigin==="anonymous"?c.credentials="omit":c.credentials="same-origin",c}function o(l){if(l.ep)return;l.ep=!0;const c=r(l);fetch(l.href,c)}})();function Of(i){return i&&i.__esModule&&Object.prototype.hasOwnProperty.call(i,"default")?i.default:i}var Zl={exports:{}},Is={},eu={exports:{}},be={};/**
 * @license React
 * react.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */var vh;function Kg(){if(vh)return be;vh=1;var i=Symbol.for("react.element"),e=Symbol.for("react.portal"),r=Symbol.for("react.fragment"),o=Symbol.for("react.strict_mode"),l=Symbol.for("react.profiler"),c=Symbol.for("react.provider"),h=Symbol.for("react.context"),m=Symbol.for("react.forward_ref"),f=Symbol.for("react.suspense"),v=Symbol.for("react.memo"),x=Symbol.for("react.lazy"),S=Symbol.iterator;function T(C){return C===null||typeof C!="object"?null:(C=S&&C[S]||C["@@iterator"],typeof C=="function"?C:null)}var R={isMounted:function(){return!1},enqueueForceUpdate:function(){},enqueueReplaceState:function(){},enqueueSetState:function(){}},P=Object.assign,b={};function A(C,O,Se){this.props=C,this.context=O,this.refs=b,this.updater=Se||R}A.prototype.isReactComponent={},A.prototype.setState=function(C,O){if(typeof C!="object"&&typeof C!="function"&&C!=null)throw Error("setState(...): takes an object of state variables to update or a function which returns an object of state variables.");this.updater.enqueueSetState(this,C,O,"setState")},A.prototype.forceUpdate=function(C){this.updater.enqueueForceUpdate(this,C,"forceUpdate")};function F(){}F.prototype=A.prototype;function se(C,O,Se){this.props=C,this.context=O,this.refs=b,this.updater=Se||R}var q=se.prototype=new F;q.constructor=se,P(q,A.prototype),q.isPureReactComponent=!0;var B=Array.isArray,W=Object.prototype.hasOwnProperty,Q={current:null},pe={key:!0,ref:!0,__self:!0,__source:!0};function de(C,O,Se){var fe,ke={},xe=null,Me=null;if(O!=null)for(fe in O.ref!==void 0&&(Me=O.ref),O.key!==void 0&&(xe=""+O.key),O)W.call(O,fe)&&!pe.hasOwnProperty(fe)&&(ke[fe]=O[fe]);var te=arguments.length-2;if(te===1)ke.children=Se;else if(1<te){for(var Le=Array(te),Ue=0;Ue<te;Ue++)Le[Ue]=arguments[Ue+2];ke.children=Le}if(C&&C.defaultProps)for(fe in te=C.defaultProps,te)ke[fe]===void 0&&(ke[fe]=te[fe]);return{$$typeof:i,type:C,key:xe,ref:Me,props:ke,_owner:Q.current}}function w(C,O){return{$$typeof:i,type:C.type,key:O,ref:C.ref,props:C.props,_owner:C._owner}}function Ne(C){return typeof C=="object"&&C!==null&&C.$$typeof===i}function we(C){var O={"=":"=0",":":"=2"};return"$"+C.replace(/[=:]/g,function(Se){return O[Se]})}var ye=/\/+/g;function me(C,O){return typeof C=="object"&&C!==null&&C.key!=null?we(""+C.key):O.toString(36)}function ue(C,O,Se,fe,ke){var xe=typeof C;(xe==="undefined"||xe==="boolean")&&(C=null);var Me=!1;if(C===null)Me=!0;else switch(xe){case"string":case"number":Me=!0;break;case"object":switch(C.$$typeof){case i:case e:Me=!0}}if(Me)return Me=C,ke=ke(Me),C=fe===""?"."+me(Me,0):fe,B(ke)?(Se="",C!=null&&(Se=C.replace(ye,"$&/")+"/"),ue(ke,O,Se,"",function(Ue){return Ue})):ke!=null&&(Ne(ke)&&(ke=w(ke,Se+(!ke.key||Me&&Me.key===ke.key?"":(""+ke.key).replace(ye,"$&/")+"/")+C)),O.push(ke)),1;if(Me=0,fe=fe===""?".":fe+":",B(C))for(var te=0;te<C.length;te++){xe=C[te];var Le=fe+me(xe,te);Me+=ue(xe,O,Se,Le,ke)}else if(Le=T(C),typeof Le=="function")for(C=Le.call(C),te=0;!(xe=C.next()).done;)xe=xe.value,Le=fe+me(xe,te++),Me+=ue(xe,O,Se,Le,ke);else if(xe==="object")throw O=String(C),Error("Objects are not valid as a React child (found: "+(O==="[object Object]"?"object with keys {"+Object.keys(C).join(", ")+"}":O)+"). If you meant to render a collection of children, use an array instead.");return Me}function Ve(C,O,Se){if(C==null)return C;var fe=[],ke=0;return ue(C,fe,"","",function(xe){return O.call(Se,xe,ke++)}),fe}function Pe(C){if(C._status===-1){var O=C._result;O=O(),O.then(function(Se){(C._status===0||C._status===-1)&&(C._status=1,C._result=Se)},function(Se){(C._status===0||C._status===-1)&&(C._status=2,C._result=Se)}),C._status===-1&&(C._status=0,C._result=O)}if(C._status===1)return C._result.default;throw C._result}var Ce={current:null},E={transition:null},ee={ReactCurrentDispatcher:Ce,ReactCurrentBatchConfig:E,ReactCurrentOwner:Q};function Y(){throw Error("act(...) is not supported in production builds of React.")}return be.Children={map:Ve,forEach:function(C,O,Se){Ve(C,function(){O.apply(this,arguments)},Se)},count:function(C){var O=0;return Ve(C,function(){O++}),O},toArray:function(C){return Ve(C,function(O){return O})||[]},only:function(C){if(!Ne(C))throw Error("React.Children.only expected to receive a single React element child.");return C}},be.Component=A,be.Fragment=r,be.Profiler=l,be.PureComponent=se,be.StrictMode=o,be.Suspense=f,be.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED=ee,be.act=Y,be.cloneElement=function(C,O,Se){if(C==null)throw Error("React.cloneElement(...): The argument must be a React element, but you passed "+C+".");var fe=P({},C.props),ke=C.key,xe=C.ref,Me=C._owner;if(O!=null){if(O.ref!==void 0&&(xe=O.ref,Me=Q.current),O.key!==void 0&&(ke=""+O.key),C.type&&C.type.defaultProps)var te=C.type.defaultProps;for(Le in O)W.call(O,Le)&&!pe.hasOwnProperty(Le)&&(fe[Le]=O[Le]===void 0&&te!==void 0?te[Le]:O[Le])}var Le=arguments.length-2;if(Le===1)fe.children=Se;else if(1<Le){te=Array(Le);for(var Ue=0;Ue<Le;Ue++)te[Ue]=arguments[Ue+2];fe.children=te}return{$$typeof:i,type:C.type,key:ke,ref:xe,props:fe,_owner:Me}},be.createContext=function(C){return C={$$typeof:h,_currentValue:C,_currentValue2:C,_threadCount:0,Provider:null,Consumer:null,_defaultValue:null,_globalName:null},C.Provider={$$typeof:c,_context:C},C.Consumer=C},be.createElement=de,be.createFactory=function(C){var O=de.bind(null,C);return O.type=C,O},be.createRef=function(){return{current:null}},be.forwardRef=function(C){return{$$typeof:m,render:C}},be.isValidElement=Ne,be.lazy=function(C){return{$$typeof:x,_payload:{_status:-1,_result:C},_init:Pe}},be.memo=function(C,O){return{$$typeof:v,type:C,compare:O===void 0?null:O}},be.startTransition=function(C){var O=E.transition;E.transition={};try{C()}finally{E.transition=O}},be.unstable_act=Y,be.useCallback=function(C,O){return Ce.current.useCallback(C,O)},be.useContext=function(C){return Ce.current.useContext(C)},be.useDebugValue=function(){},be.useDeferredValue=function(C){return Ce.current.useDeferredValue(C)},be.useEffect=function(C,O){return Ce.current.useEffect(C,O)},be.useId=function(){return Ce.current.useId()},be.useImperativeHandle=function(C,O,Se){return Ce.current.useImperativeHandle(C,O,Se)},be.useInsertionEffect=function(C,O){return Ce.current.useInsertionEffect(C,O)},be.useLayoutEffect=function(C,O){return Ce.current.useLayoutEffect(C,O)},be.useMemo=function(C,O){return Ce.current.useMemo(C,O)},be.useReducer=function(C,O,Se){return Ce.current.useReducer(C,O,Se)},be.useRef=function(C){return Ce.current.useRef(C)},be.useState=function(C){return Ce.current.useState(C)},be.useSyncExternalStore=function(C,O,Se){return Ce.current.useSyncExternalStore(C,O,Se)},be.useTransition=function(){return Ce.current.useTransition()},be.version="18.3.1",be}var yh;function Du(){return yh||(yh=1,eu.exports=Kg()),eu.exports}/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */var wh;function Xg(){if(wh)return Is;wh=1;var i=Du(),e=Symbol.for("react.element"),r=Symbol.for("react.fragment"),o=Object.prototype.hasOwnProperty,l=i.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner,c={key:!0,ref:!0,__self:!0,__source:!0};function h(m,f,v){var x,S={},T=null,R=null;v!==void 0&&(T=""+v),f.key!==void 0&&(T=""+f.key),f.ref!==void 0&&(R=f.ref);for(x in f)o.call(f,x)&&!c.hasOwnProperty(x)&&(S[x]=f[x]);if(m&&m.defaultProps)for(x in f=m.defaultProps,f)S[x]===void 0&&(S[x]=f[x]);return{$$typeof:e,type:m,key:T,ref:R,props:S,_owner:l.current}}return Is.Fragment=r,Is.jsx=h,Is.jsxs=h,Is}var xh;function Yg(){return xh||(xh=1,Zl.exports=Xg()),Zl.exports}var g=Yg(),ne=Du();const Qg=Of(ne);var qo={},tu={exports:{}},Gt={},nu={exports:{}},ru={};/**
 * @license React
 * scheduler.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */var _h;function Jg(){return _h||(_h=1,(function(i){function e(E,ee){var Y=E.length;E.push(ee);e:for(;0<Y;){var C=Y-1>>>1,O=E[C];if(0<l(O,ee))E[C]=ee,E[Y]=O,Y=C;else break e}}function r(E){return E.length===0?null:E[0]}function o(E){if(E.length===0)return null;var ee=E[0],Y=E.pop();if(Y!==ee){E[0]=Y;e:for(var C=0,O=E.length,Se=O>>>1;C<Se;){var fe=2*(C+1)-1,ke=E[fe],xe=fe+1,Me=E[xe];if(0>l(ke,Y))xe<O&&0>l(Me,ke)?(E[C]=Me,E[xe]=Y,C=xe):(E[C]=ke,E[fe]=Y,C=fe);else if(xe<O&&0>l(Me,Y))E[C]=Me,E[xe]=Y,C=xe;else break e}}return ee}function l(E,ee){var Y=E.sortIndex-ee.sortIndex;return Y!==0?Y:E.id-ee.id}if(typeof performance=="object"&&typeof performance.now=="function"){var c=performance;i.unstable_now=function(){return c.now()}}else{var h=Date,m=h.now();i.unstable_now=function(){return h.now()-m}}var f=[],v=[],x=1,S=null,T=3,R=!1,P=!1,b=!1,A=typeof setTimeout=="function"?setTimeout:null,F=typeof clearTimeout=="function"?clearTimeout:null,se=typeof setImmediate<"u"?setImmediate:null;typeof navigator<"u"&&navigator.scheduling!==void 0&&navigator.scheduling.isInputPending!==void 0&&navigator.scheduling.isInputPending.bind(navigator.scheduling);function q(E){for(var ee=r(v);ee!==null;){if(ee.callback===null)o(v);else if(ee.startTime<=E)o(v),ee.sortIndex=ee.expirationTime,e(f,ee);else break;ee=r(v)}}function B(E){if(b=!1,q(E),!P)if(r(f)!==null)P=!0,Pe(W);else{var ee=r(v);ee!==null&&Ce(B,ee.startTime-E)}}function W(E,ee){P=!1,b&&(b=!1,F(de),de=-1),R=!0;var Y=T;try{for(q(ee),S=r(f);S!==null&&(!(S.expirationTime>ee)||E&&!we());){var C=S.callback;if(typeof C=="function"){S.callback=null,T=S.priorityLevel;var O=C(S.expirationTime<=ee);ee=i.unstable_now(),typeof O=="function"?S.callback=O:S===r(f)&&o(f),q(ee)}else o(f);S=r(f)}if(S!==null)var Se=!0;else{var fe=r(v);fe!==null&&Ce(B,fe.startTime-ee),Se=!1}return Se}finally{S=null,T=Y,R=!1}}var Q=!1,pe=null,de=-1,w=5,Ne=-1;function we(){return!(i.unstable_now()-Ne<w)}function ye(){if(pe!==null){var E=i.unstable_now();Ne=E;var ee=!0;try{ee=pe(!0,E)}finally{ee?me():(Q=!1,pe=null)}}else Q=!1}var me;if(typeof se=="function")me=function(){se(ye)};else if(typeof MessageChannel<"u"){var ue=new MessageChannel,Ve=ue.port2;ue.port1.onmessage=ye,me=function(){Ve.postMessage(null)}}else me=function(){A(ye,0)};function Pe(E){pe=E,Q||(Q=!0,me())}function Ce(E,ee){de=A(function(){E(i.unstable_now())},ee)}i.unstable_IdlePriority=5,i.unstable_ImmediatePriority=1,i.unstable_LowPriority=4,i.unstable_NormalPriority=3,i.unstable_Profiling=null,i.unstable_UserBlockingPriority=2,i.unstable_cancelCallback=function(E){E.callback=null},i.unstable_continueExecution=function(){P||R||(P=!0,Pe(W))},i.unstable_forceFrameRate=function(E){0>E||125<E?console.error("forceFrameRate takes a positive int between 0 and 125, forcing frame rates higher than 125 fps is not supported"):w=0<E?Math.floor(1e3/E):5},i.unstable_getCurrentPriorityLevel=function(){return T},i.unstable_getFirstCallbackNode=function(){return r(f)},i.unstable_next=function(E){switch(T){case 1:case 2:case 3:var ee=3;break;default:ee=T}var Y=T;T=ee;try{return E()}finally{T=Y}},i.unstable_pauseExecution=function(){},i.unstable_requestPaint=function(){},i.unstable_runWithPriority=function(E,ee){switch(E){case 1:case 2:case 3:case 4:case 5:break;default:E=3}var Y=T;T=E;try{return ee()}finally{T=Y}},i.unstable_scheduleCallback=function(E,ee,Y){var C=i.unstable_now();switch(typeof Y=="object"&&Y!==null?(Y=Y.delay,Y=typeof Y=="number"&&0<Y?C+Y:C):Y=C,E){case 1:var O=-1;break;case 2:O=250;break;case 5:O=1073741823;break;case 4:O=1e4;break;default:O=5e3}return O=Y+O,E={id:x++,callback:ee,priorityLevel:E,startTime:Y,expirationTime:O,sortIndex:-1},Y>C?(E.sortIndex=Y,e(v,E),r(f)===null&&E===r(v)&&(b?(F(de),de=-1):b=!0,Ce(B,Y-C))):(E.sortIndex=O,e(f,E),P||R||(P=!0,Pe(W))),E},i.unstable_shouldYield=we,i.unstable_wrapCallback=function(E){var ee=T;return function(){var Y=T;T=ee;try{return E.apply(this,arguments)}finally{T=Y}}}})(ru)),ru}var Eh;function Zg(){return Eh||(Eh=1,nu.exports=Jg()),nu.exports}/**
 * @license React
 * react-dom.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */var Sh;function e0(){if(Sh)return Gt;Sh=1;var i=Du(),e=Zg();function r(t){for(var n="https://reactjs.org/docs/error-decoder.html?invariant="+t,s=1;s<arguments.length;s++)n+="&args[]="+encodeURIComponent(arguments[s]);return"Minified React error #"+t+"; visit "+n+" for the full message or use the non-minified dev environment for full errors and additional helpful warnings."}var o=new Set,l={};function c(t,n){h(t,n),h(t+"Capture",n)}function h(t,n){for(l[t]=n,t=0;t<n.length;t++)o.add(n[t])}var m=!(typeof window>"u"||typeof window.document>"u"||typeof window.document.createElement>"u"),f=Object.prototype.hasOwnProperty,v=/^[:A-Z_a-z\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u02FF\u0370-\u037D\u037F-\u1FFF\u200C-\u200D\u2070-\u218F\u2C00-\u2FEF\u3001-\uD7FF\uF900-\uFDCF\uFDF0-\uFFFD][:A-Z_a-z\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u02FF\u0370-\u037D\u037F-\u1FFF\u200C-\u200D\u2070-\u218F\u2C00-\u2FEF\u3001-\uD7FF\uF900-\uFDCF\uFDF0-\uFFFD\-.0-9\u00B7\u0300-\u036F\u203F-\u2040]*$/,x={},S={};function T(t){return f.call(S,t)?!0:f.call(x,t)?!1:v.test(t)?S[t]=!0:(x[t]=!0,!1)}function R(t,n,s,a){if(s!==null&&s.type===0)return!1;switch(typeof n){case"function":case"symbol":return!0;case"boolean":return a?!1:s!==null?!s.acceptsBooleans:(t=t.toLowerCase().slice(0,5),t!=="data-"&&t!=="aria-");default:return!1}}function P(t,n,s,a){if(n===null||typeof n>"u"||R(t,n,s,a))return!0;if(a)return!1;if(s!==null)switch(s.type){case 3:return!n;case 4:return n===!1;case 5:return isNaN(n);case 6:return isNaN(n)||1>n}return!1}function b(t,n,s,a,u,d,p){this.acceptsBooleans=n===2||n===3||n===4,this.attributeName=a,this.attributeNamespace=u,this.mustUseProperty=s,this.propertyName=t,this.type=n,this.sanitizeURL=d,this.removeEmptyString=p}var A={};"children dangerouslySetInnerHTML defaultValue defaultChecked innerHTML suppressContentEditableWarning suppressHydrationWarning style".split(" ").forEach(function(t){A[t]=new b(t,0,!1,t,null,!1,!1)}),[["acceptCharset","accept-charset"],["className","class"],["htmlFor","for"],["httpEquiv","http-equiv"]].forEach(function(t){var n=t[0];A[n]=new b(n,1,!1,t[1],null,!1,!1)}),["contentEditable","draggable","spellCheck","value"].forEach(function(t){A[t]=new b(t,2,!1,t.toLowerCase(),null,!1,!1)}),["autoReverse","externalResourcesRequired","focusable","preserveAlpha"].forEach(function(t){A[t]=new b(t,2,!1,t,null,!1,!1)}),"allowFullScreen async autoFocus autoPlay controls default defer disabled disablePictureInPicture disableRemotePlayback formNoValidate hidden loop noModule noValidate open playsInline readOnly required reversed scoped seamless itemScope".split(" ").forEach(function(t){A[t]=new b(t,3,!1,t.toLowerCase(),null,!1,!1)}),["checked","multiple","muted","selected"].forEach(function(t){A[t]=new b(t,3,!0,t,null,!1,!1)}),["capture","download"].forEach(function(t){A[t]=new b(t,4,!1,t,null,!1,!1)}),["cols","rows","size","span"].forEach(function(t){A[t]=new b(t,6,!1,t,null,!1,!1)}),["rowSpan","start"].forEach(function(t){A[t]=new b(t,5,!1,t.toLowerCase(),null,!1,!1)});var F=/[\-:]([a-z])/g;function se(t){return t[1].toUpperCase()}"accent-height alignment-baseline arabic-form baseline-shift cap-height clip-path clip-rule color-interpolation color-interpolation-filters color-profile color-rendering dominant-baseline enable-background fill-opacity fill-rule flood-color flood-opacity font-family font-size font-size-adjust font-stretch font-style font-variant font-weight glyph-name glyph-orientation-horizontal glyph-orientation-vertical horiz-adv-x horiz-origin-x image-rendering letter-spacing lighting-color marker-end marker-mid marker-start overline-position overline-thickness paint-order panose-1 pointer-events rendering-intent shape-rendering stop-color stop-opacity strikethrough-position strikethrough-thickness stroke-dasharray stroke-dashoffset stroke-linecap stroke-linejoin stroke-miterlimit stroke-opacity stroke-width text-anchor text-decoration text-rendering underline-position underline-thickness unicode-bidi unicode-range units-per-em v-alphabetic v-hanging v-ideographic v-mathematical vector-effect vert-adv-y vert-origin-x vert-origin-y word-spacing writing-mode xmlns:xlink x-height".split(" ").forEach(function(t){var n=t.replace(F,se);A[n]=new b(n,1,!1,t,null,!1,!1)}),"xlink:actuate xlink:arcrole xlink:role xlink:show xlink:title xlink:type".split(" ").forEach(function(t){var n=t.replace(F,se);A[n]=new b(n,1,!1,t,"http://www.w3.org/1999/xlink",!1,!1)}),["xml:base","xml:lang","xml:space"].forEach(function(t){var n=t.replace(F,se);A[n]=new b(n,1,!1,t,"http://www.w3.org/XML/1998/namespace",!1,!1)}),["tabIndex","crossOrigin"].forEach(function(t){A[t]=new b(t,1,!1,t.toLowerCase(),null,!1,!1)}),A.xlinkHref=new b("xlinkHref",1,!1,"xlink:href","http://www.w3.org/1999/xlink",!0,!1),["src","href","action","formAction"].forEach(function(t){A[t]=new b(t,1,!1,t.toLowerCase(),null,!0,!0)});function q(t,n,s,a){var u=A.hasOwnProperty(n)?A[n]:null;(u!==null?u.type!==0:a||!(2<n.length)||n[0]!=="o"&&n[0]!=="O"||n[1]!=="n"&&n[1]!=="N")&&(P(n,s,u,a)&&(s=null),a||u===null?T(n)&&(s===null?t.removeAttribute(n):t.setAttribute(n,""+s)):u.mustUseProperty?t[u.propertyName]=s===null?u.type===3?!1:"":s:(n=u.attributeName,a=u.attributeNamespace,s===null?t.removeAttribute(n):(u=u.type,s=u===3||u===4&&s===!0?"":""+s,a?t.setAttributeNS(a,n,s):t.setAttribute(n,s))))}var B=i.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED,W=Symbol.for("react.element"),Q=Symbol.for("react.portal"),pe=Symbol.for("react.fragment"),de=Symbol.for("react.strict_mode"),w=Symbol.for("react.profiler"),Ne=Symbol.for("react.provider"),we=Symbol.for("react.context"),ye=Symbol.for("react.forward_ref"),me=Symbol.for("react.suspense"),ue=Symbol.for("react.suspense_list"),Ve=Symbol.for("react.memo"),Pe=Symbol.for("react.lazy"),Ce=Symbol.for("react.offscreen"),E=Symbol.iterator;function ee(t){return t===null||typeof t!="object"?null:(t=E&&t[E]||t["@@iterator"],typeof t=="function"?t:null)}var Y=Object.assign,C;function O(t){if(C===void 0)try{throw Error()}catch(s){var n=s.stack.trim().match(/\n( *(at )?)/);C=n&&n[1]||""}return`
`+C+t}var Se=!1;function fe(t,n){if(!t||Se)return"";Se=!0;var s=Error.prepareStackTrace;Error.prepareStackTrace=void 0;try{if(n)if(n=function(){throw Error()},Object.defineProperty(n.prototype,"props",{set:function(){throw Error()}}),typeof Reflect=="object"&&Reflect.construct){try{Reflect.construct(n,[])}catch(M){var a=M}Reflect.construct(t,[],n)}else{try{n.call()}catch(M){a=M}t.call(n.prototype)}else{try{throw Error()}catch(M){a=M}t()}}catch(M){if(M&&a&&typeof M.stack=="string"){for(var u=M.stack.split(`
`),d=a.stack.split(`
`),p=u.length-1,y=d.length-1;1<=p&&0<=y&&u[p]!==d[y];)y--;for(;1<=p&&0<=y;p--,y--)if(u[p]!==d[y]){if(p!==1||y!==1)do if(p--,y--,0>y||u[p]!==d[y]){var _=`
`+u[p].replace(" at new "," at ");return t.displayName&&_.includes("<anonymous>")&&(_=_.replace("<anonymous>",t.displayName)),_}while(1<=p&&0<=y);break}}}finally{Se=!1,Error.prepareStackTrace=s}return(t=t?t.displayName||t.name:"")?O(t):""}function ke(t){switch(t.tag){case 5:return O(t.type);case 16:return O("Lazy");case 13:return O("Suspense");case 19:return O("SuspenseList");case 0:case 2:case 15:return t=fe(t.type,!1),t;case 11:return t=fe(t.type.render,!1),t;case 1:return t=fe(t.type,!0),t;default:return""}}function xe(t){if(t==null)return null;if(typeof t=="function")return t.displayName||t.name||null;if(typeof t=="string")return t;switch(t){case pe:return"Fragment";case Q:return"Portal";case w:return"Profiler";case de:return"StrictMode";case me:return"Suspense";case ue:return"SuspenseList"}if(typeof t=="object")switch(t.$$typeof){case we:return(t.displayName||"Context")+".Consumer";case Ne:return(t._context.displayName||"Context")+".Provider";case ye:var n=t.render;return t=t.displayName,t||(t=n.displayName||n.name||"",t=t!==""?"ForwardRef("+t+")":"ForwardRef"),t;case Ve:return n=t.displayName||null,n!==null?n:xe(t.type)||"Memo";case Pe:n=t._payload,t=t._init;try{return xe(t(n))}catch{}}return null}function Me(t){var n=t.type;switch(t.tag){case 24:return"Cache";case 9:return(n.displayName||"Context")+".Consumer";case 10:return(n._context.displayName||"Context")+".Provider";case 18:return"DehydratedFragment";case 11:return t=n.render,t=t.displayName||t.name||"",n.displayName||(t!==""?"ForwardRef("+t+")":"ForwardRef");case 7:return"Fragment";case 5:return n;case 4:return"Portal";case 3:return"Root";case 6:return"Text";case 16:return xe(n);case 8:return n===de?"StrictMode":"Mode";case 22:return"Offscreen";case 12:return"Profiler";case 21:return"Scope";case 13:return"Suspense";case 19:return"SuspenseList";case 25:return"TracingMarker";case 1:case 0:case 17:case 2:case 14:case 15:if(typeof n=="function")return n.displayName||n.name||null;if(typeof n=="string")return n}return null}function te(t){switch(typeof t){case"boolean":case"number":case"string":case"undefined":return t;case"object":return t;default:return""}}function Le(t){var n=t.type;return(t=t.nodeName)&&t.toLowerCase()==="input"&&(n==="checkbox"||n==="radio")}function Ue(t){var n=Le(t)?"checked":"value",s=Object.getOwnPropertyDescriptor(t.constructor.prototype,n),a=""+t[n];if(!t.hasOwnProperty(n)&&typeof s<"u"&&typeof s.get=="function"&&typeof s.set=="function"){var u=s.get,d=s.set;return Object.defineProperty(t,n,{configurable:!0,get:function(){return u.call(this)},set:function(p){a=""+p,d.call(this,p)}}),Object.defineProperty(t,n,{enumerable:s.enumerable}),{getValue:function(){return a},setValue:function(p){a=""+p},stopTracking:function(){t._valueTracker=null,delete t[n]}}}}function He(t){t._valueTracker||(t._valueTracker=Ue(t))}function nt(t){if(!t)return!1;var n=t._valueTracker;if(!n)return!0;var s=n.getValue(),a="";return t&&(a=Le(t)?t.checked?"true":"false":t.value),t=a,t!==s?(n.setValue(t),!0):!1}function Qe(t){if(t=t||(typeof document<"u"?document:void 0),typeof t>"u")return null;try{return t.activeElement||t.body}catch{return t.body}}function Be(t,n){var s=n.checked;return Y({},n,{defaultChecked:void 0,defaultValue:void 0,value:void 0,checked:s??t._wrapperState.initialChecked})}function sn(t,n){var s=n.defaultValue==null?"":n.defaultValue,a=n.checked!=null?n.checked:n.defaultChecked;s=te(n.value!=null?n.value:s),t._wrapperState={initialChecked:a,initialValue:s,controlled:n.type==="checkbox"||n.type==="radio"?n.checked!=null:n.value!=null}}function vt(t,n){n=n.checked,n!=null&&q(t,"checked",n,!1)}function qt(t,n){vt(t,n);var s=te(n.value),a=n.type;if(s!=null)a==="number"?(s===0&&t.value===""||t.value!=s)&&(t.value=""+s):t.value!==""+s&&(t.value=""+s);else if(a==="submit"||a==="reset"){t.removeAttribute("value");return}n.hasOwnProperty("value")?Hn(t,n.type,s):n.hasOwnProperty("defaultValue")&&Hn(t,n.type,te(n.defaultValue)),n.checked==null&&n.defaultChecked!=null&&(t.defaultChecked=!!n.defaultChecked)}function Mn(t,n,s){if(n.hasOwnProperty("value")||n.hasOwnProperty("defaultValue")){var a=n.type;if(!(a!=="submit"&&a!=="reset"||n.value!==void 0&&n.value!==null))return;n=""+t._wrapperState.initialValue,s||n===t.value||(t.value=n),t.defaultValue=n}s=t.name,s!==""&&(t.name=""),t.defaultChecked=!!t._wrapperState.initialChecked,s!==""&&(t.name=s)}function Hn(t,n,s){(n!=="number"||Qe(t.ownerDocument)!==t)&&(s==null?t.defaultValue=""+t._wrapperState.initialValue:t.defaultValue!==""+s&&(t.defaultValue=""+s))}var on=Array.isArray;function Fe(t,n,s,a){if(t=t.options,n){n={};for(var u=0;u<s.length;u++)n["$"+s[u]]=!0;for(s=0;s<t.length;s++)u=n.hasOwnProperty("$"+t[s].value),t[s].selected!==u&&(t[s].selected=u),u&&a&&(t[s].defaultSelected=!0)}else{for(s=""+te(s),n=null,u=0;u<t.length;u++){if(t[u].value===s){t[u].selected=!0,a&&(t[u].defaultSelected=!0);return}n!==null||t[u].disabled||(n=t[u])}n!==null&&(n.selected=!0)}}function Ot(t,n){if(n.dangerouslySetInnerHTML!=null)throw Error(r(91));return Y({},n,{value:void 0,defaultValue:void 0,children:""+t._wrapperState.initialValue})}function an(t,n){var s=n.value;if(s==null){if(s=n.children,n=n.defaultValue,s!=null){if(n!=null)throw Error(r(92));if(on(s)){if(1<s.length)throw Error(r(93));s=s[0]}n=s}n==null&&(n=""),s=n}t._wrapperState={initialValue:te(s)}}function Wn(t,n){var s=te(n.value),a=te(n.defaultValue);s!=null&&(s=""+s,s!==t.value&&(t.value=s),n.defaultValue==null&&t.defaultValue!==s&&(t.defaultValue=s)),a!=null&&(t.defaultValue=""+a)}function ot(t){var n=t.textContent;n===t._wrapperState.initialValue&&n!==""&&n!==null&&(t.value=n)}function it(t){switch(t){case"svg":return"http://www.w3.org/2000/svg";case"math":return"http://www.w3.org/1998/Math/MathML";default:return"http://www.w3.org/1999/xhtml"}}function ft(t,n){return t==null||t==="http://www.w3.org/1999/xhtml"?it(n):t==="http://www.w3.org/2000/svg"&&n==="foreignObject"?"http://www.w3.org/1999/xhtml":t}var at,Kt=(function(t){return typeof MSApp<"u"&&MSApp.execUnsafeLocalFunction?function(n,s,a,u){MSApp.execUnsafeLocalFunction(function(){return t(n,s,a,u)})}:t})(function(t,n){if(t.namespaceURI!=="http://www.w3.org/2000/svg"||"innerHTML"in t)t.innerHTML=n;else{for(at=at||document.createElement("div"),at.innerHTML="<svg>"+n.valueOf().toString()+"</svg>",n=at.firstChild;t.firstChild;)t.removeChild(t.firstChild);for(;n.firstChild;)t.appendChild(n.firstChild)}});function Ft(t,n){if(n){var s=t.firstChild;if(s&&s===t.lastChild&&s.nodeType===3){s.nodeValue=n;return}}t.textContent=n}var Nt={animationIterationCount:!0,aspectRatio:!0,borderImageOutset:!0,borderImageSlice:!0,borderImageWidth:!0,boxFlex:!0,boxFlexGroup:!0,boxOrdinalGroup:!0,columnCount:!0,columns:!0,flex:!0,flexGrow:!0,flexPositive:!0,flexShrink:!0,flexNegative:!0,flexOrder:!0,gridArea:!0,gridRow:!0,gridRowEnd:!0,gridRowSpan:!0,gridRowStart:!0,gridColumn:!0,gridColumnEnd:!0,gridColumnSpan:!0,gridColumnStart:!0,fontWeight:!0,lineClamp:!0,lineHeight:!0,opacity:!0,order:!0,orphans:!0,tabSize:!0,widows:!0,zIndex:!0,zoom:!0,fillOpacity:!0,floodOpacity:!0,stopOpacity:!0,strokeDasharray:!0,strokeDashoffset:!0,strokeMiterlimit:!0,strokeOpacity:!0,strokeWidth:!0},Et=["Webkit","ms","Moz","O"];Object.keys(Nt).forEach(function(t){Et.forEach(function(n){n=n+t.charAt(0).toUpperCase()+t.substring(1),Nt[n]=Nt[t]})});function L(t,n,s){return n==null||typeof n=="boolean"||n===""?"":s||typeof n!="number"||n===0||Nt.hasOwnProperty(t)&&Nt[t]?(""+n).trim():n+"px"}function G(t,n){t=t.style;for(var s in n)if(n.hasOwnProperty(s)){var a=s.indexOf("--")===0,u=L(s,n[s],a);s==="float"&&(s="cssFloat"),a?t.setProperty(s,u):t[s]=u}}var j=Y({menuitem:!0},{area:!0,base:!0,br:!0,col:!0,embed:!0,hr:!0,img:!0,input:!0,keygen:!0,link:!0,meta:!0,param:!0,source:!0,track:!0,wbr:!0});function V(t,n){if(n){if(j[t]&&(n.children!=null||n.dangerouslySetInnerHTML!=null))throw Error(r(137,t));if(n.dangerouslySetInnerHTML!=null){if(n.children!=null)throw Error(r(60));if(typeof n.dangerouslySetInnerHTML!="object"||!("__html"in n.dangerouslySetInnerHTML))throw Error(r(61))}if(n.style!=null&&typeof n.style!="object")throw Error(r(62))}}function J(t,n){if(t.indexOf("-")===-1)return typeof n.is=="string";switch(t){case"annotation-xml":case"color-profile":case"font-face":case"font-face-src":case"font-face-uri":case"font-face-format":case"font-face-name":case"missing-glyph":return!1;default:return!0}}var oe=null;function Te(t){return t=t.target||t.srcElement||window,t.correspondingUseElement&&(t=t.correspondingUseElement),t.nodeType===3?t.parentNode:t}var De=null,D=null,K=null;function H(t){if(t=hs(t)){if(typeof De!="function")throw Error(r(280));var n=t.stateNode;n&&(n=ao(n),De(t.stateNode,t.type,n))}}function he(t){D?K?K.push(t):K=[t]:D=t}function _e(){if(D){var t=D,n=K;if(K=D=null,H(t),n)for(t=0;t<n.length;t++)H(n[t])}}function Re(t,n){return t(n)}function yt(){}var Xt=!1;function ln(t,n,s){if(Xt)return t(n,s);Xt=!0;try{return Re(t,n,s)}finally{Xt=!1,(D!==null||K!==null)&&(yt(),_e())}}function lt(t,n){var s=t.stateNode;if(s===null)return null;var a=ao(s);if(a===null)return null;s=a[n];e:switch(n){case"onClick":case"onClickCapture":case"onDoubleClick":case"onDoubleClickCapture":case"onMouseDown":case"onMouseDownCapture":case"onMouseMove":case"onMouseMoveCapture":case"onMouseUp":case"onMouseUpCapture":case"onMouseEnter":(a=!a.disabled)||(t=t.type,a=!(t==="button"||t==="input"||t==="select"||t==="textarea")),t=!a;break e;default:t=!1}if(t)return null;if(s&&typeof s!="function")throw Error(r(231,n,typeof s));return s}var wt=!1;if(m)try{var zt={};Object.defineProperty(zt,"passive",{get:function(){wt=!0}}),window.addEventListener("test",zt,zt),window.removeEventListener("test",zt,zt)}catch{wt=!1}function yn(t,n,s,a,u,d,p,y,_){var M=Array.prototype.slice.call(arguments,3);try{n.apply(s,M)}catch(U){this.onError(U)}}var un=!1,Dn=null,St=!1,Gn=null,dr={onError:function(t){un=!0,Dn=t}};function hr(t,n,s,a,u,d,p,y,_){un=!1,Dn=null,yn.apply(dr,arguments)}function Hs(t,n,s,a,u,d,p,y,_){if(hr.apply(this,arguments),un){if(un){var M=Dn;un=!1,Dn=null}else throw Error(r(198));St||(St=!0,Gn=M)}}function bn(t){var n=t,s=t;if(t.alternate)for(;n.return;)n=n.return;else{t=n;do n=t,(n.flags&4098)!==0&&(s=n.return),t=n.return;while(t)}return n.tag===3?s:null}function Oe(t){if(t.tag===13){var n=t.memoizedState;if(n===null&&(t=t.alternate,t!==null&&(n=t.memoizedState)),n!==null)return n.dehydrated}return null}function ce(t){if(bn(t)!==t)throw Error(r(188))}function Ae(t){var n=t.alternate;if(!n){if(n=bn(t),n===null)throw Error(r(188));return n!==t?null:t}for(var s=t,a=n;;){var u=s.return;if(u===null)break;var d=u.alternate;if(d===null){if(a=u.return,a!==null){s=a;continue}break}if(u.child===d.child){for(d=u.child;d;){if(d===s)return ce(u),t;if(d===a)return ce(u),n;d=d.sibling}throw Error(r(188))}if(s.return!==a.return)s=u,a=d;else{for(var p=!1,y=u.child;y;){if(y===s){p=!0,s=u,a=d;break}if(y===a){p=!0,a=u,s=d;break}y=y.sibling}if(!p){for(y=d.child;y;){if(y===s){p=!0,s=d,a=u;break}if(y===a){p=!0,a=d,s=u;break}y=y.sibling}if(!p)throw Error(r(189))}}if(s.alternate!==a)throw Error(r(190))}if(s.tag!==3)throw Error(r(188));return s.stateNode.current===s?t:n}function Pt(t){return t=Ae(t),t!==null?At(t):null}function At(t){if(t.tag===5||t.tag===6)return t;for(t=t.child;t!==null;){var n=At(t);if(n!==null)return n;t=t.sibling}return null}var Yt=e.unstable_scheduleCallback,di=e.unstable_cancelCallback,Qt=e.unstable_shouldYield,fr=e.unstable_requestPaint,Ge=e.unstable_now,hi=e.unstable_getCurrentPriorityLevel,Gi=e.unstable_ImmediatePriority,fi=e.unstable_UserBlockingPriority,pi=e.unstable_NormalPriority,_a=e.unstable_LowPriority,qn=e.unstable_IdlePriority,wn=null,Jt=null;function qi(t){if(Jt&&typeof Jt.onCommitFiberRoot=="function")try{Jt.onCommitFiberRoot(wn,t,void 0,(t.current.flags&128)===128)}catch{}}var jt=Math.clz32?Math.clz32:cn,Ea=Math.log,Ws=Math.LN2;function cn(t){return t>>>=0,t===0?32:31-(Ea(t)/Ws|0)|0}var $r=64,Vr=4194304;function pr(t){switch(t&-t){case 1:return 1;case 2:return 2;case 4:return 4;case 8:return 8;case 16:return 16;case 32:return 32;case 64:case 128:case 256:case 512:case 1024:case 2048:case 4096:case 8192:case 16384:case 32768:case 65536:case 131072:case 262144:case 524288:case 1048576:case 2097152:return t&4194240;case 4194304:case 8388608:case 16777216:case 33554432:case 67108864:return t&130023424;case 134217728:return 134217728;case 268435456:return 268435456;case 536870912:return 536870912;case 1073741824:return 1073741824;default:return t}}function Hr(t,n){var s=t.pendingLanes;if(s===0)return 0;var a=0,u=t.suspendedLanes,d=t.pingedLanes,p=s&268435455;if(p!==0){var y=p&~u;y!==0?a=pr(y):(d&=p,d!==0&&(a=pr(d)))}else p=s&~u,p!==0?a=pr(p):d!==0&&(a=pr(d));if(a===0)return 0;if(n!==0&&n!==a&&(n&u)===0&&(u=a&-a,d=n&-n,u>=d||u===16&&(d&4194240)!==0))return n;if((a&4)!==0&&(a|=s&16),n=t.entangledLanes,n!==0)for(t=t.entanglements,n&=a;0<n;)s=31-jt(n),u=1<<s,a|=t[s],n&=~u;return a}function kt(t,n){switch(t){case 1:case 2:case 4:return n+250;case 8:case 16:case 32:case 64:case 128:case 256:case 512:case 1024:case 2048:case 4096:case 8192:case 16384:case 32768:case 65536:case 131072:case 262144:case 524288:case 1048576:case 2097152:return n+5e3;case 4194304:case 8388608:case 16777216:case 33554432:case 67108864:return-1;case 134217728:case 268435456:case 536870912:case 1073741824:return-1;default:return-1}}function Ki(t,n){for(var s=t.suspendedLanes,a=t.pingedLanes,u=t.expirationTimes,d=t.pendingLanes;0<d;){var p=31-jt(d),y=1<<p,_=u[p];_===-1?((y&s)===0||(y&a)!==0)&&(u[p]=kt(y,n)):_<=n&&(t.expiredLanes|=y),d&=~y}}function Xi(t){return t=t.pendingLanes&-1073741825,t!==0?t:t&1073741824?1073741824:0}function Ut(){var t=$r;return $r<<=1,($r&4194240)===0&&($r=64),t}function ct(t){for(var n=[],s=0;31>s;s++)n.push(t);return n}function Wr(t,n,s){t.pendingLanes|=n,n!==536870912&&(t.suspendedLanes=0,t.pingedLanes=0),t=t.eventTimes,n=31-jt(n),t[n]=s}function Kn(t,n){var s=t.pendingLanes&~n;t.pendingLanes=n,t.suspendedLanes=0,t.pingedLanes=0,t.expiredLanes&=n,t.mutableReadLanes&=n,t.entangledLanes&=n,n=t.entanglements;var a=t.eventTimes;for(t=t.expirationTimes;0<s;){var u=31-jt(s),d=1<<u;n[u]=0,a[u]=-1,t[u]=-1,s&=~d}}function xn(t,n){var s=t.entangledLanes|=n;for(t=t.entanglements;s;){var a=31-jt(s),u=1<<a;u&n|t[a]&n&&(t[a]|=n),s&=~u}}var $e=0;function Xu(t){return t&=-t,1<t?4<t?(t&268435455)!==0?16:536870912:4:1}var Yu,Sa,Qu,Ju,Zu,ka=!1,Gs=[],mr=null,gr=null,vr=null,Yi=new Map,Qi=new Map,yr=[],gm="mousedown mouseup touchcancel touchend touchstart auxclick dblclick pointercancel pointerdown pointerup dragend dragstart drop compositionend compositionstart keydown keypress keyup input textInput copy cut paste click change contextmenu reset submit".split(" ");function ec(t,n){switch(t){case"focusin":case"focusout":mr=null;break;case"dragenter":case"dragleave":gr=null;break;case"mouseover":case"mouseout":vr=null;break;case"pointerover":case"pointerout":Yi.delete(n.pointerId);break;case"gotpointercapture":case"lostpointercapture":Qi.delete(n.pointerId)}}function Ji(t,n,s,a,u,d){return t===null||t.nativeEvent!==d?(t={blockedOn:n,domEventName:s,eventSystemFlags:a,nativeEvent:d,targetContainers:[u]},n!==null&&(n=hs(n),n!==null&&Sa(n)),t):(t.eventSystemFlags|=a,n=t.targetContainers,u!==null&&n.indexOf(u)===-1&&n.push(u),t)}function vm(t,n,s,a,u){switch(n){case"focusin":return mr=Ji(mr,t,n,s,a,u),!0;case"dragenter":return gr=Ji(gr,t,n,s,a,u),!0;case"mouseover":return vr=Ji(vr,t,n,s,a,u),!0;case"pointerover":var d=u.pointerId;return Yi.set(d,Ji(Yi.get(d)||null,t,n,s,a,u)),!0;case"gotpointercapture":return d=u.pointerId,Qi.set(d,Ji(Qi.get(d)||null,t,n,s,a,u)),!0}return!1}function tc(t){var n=Gr(t.target);if(n!==null){var s=bn(n);if(s!==null){if(n=s.tag,n===13){if(n=Oe(s),n!==null){t.blockedOn=n,Zu(t.priority,function(){Qu(s)});return}}else if(n===3&&s.stateNode.current.memoizedState.isDehydrated){t.blockedOn=s.tag===3?s.stateNode.containerInfo:null;return}}}t.blockedOn=null}function qs(t){if(t.blockedOn!==null)return!1;for(var n=t.targetContainers;0<n.length;){var s=Ca(t.domEventName,t.eventSystemFlags,n[0],t.nativeEvent);if(s===null){s=t.nativeEvent;var a=new s.constructor(s.type,s);oe=a,s.target.dispatchEvent(a),oe=null}else return n=hs(s),n!==null&&Sa(n),t.blockedOn=s,!1;n.shift()}return!0}function nc(t,n,s){qs(t)&&s.delete(n)}function ym(){ka=!1,mr!==null&&qs(mr)&&(mr=null),gr!==null&&qs(gr)&&(gr=null),vr!==null&&qs(vr)&&(vr=null),Yi.forEach(nc),Qi.forEach(nc)}function Zi(t,n){t.blockedOn===n&&(t.blockedOn=null,ka||(ka=!0,e.unstable_scheduleCallback(e.unstable_NormalPriority,ym)))}function es(t){function n(u){return Zi(u,t)}if(0<Gs.length){Zi(Gs[0],t);for(var s=1;s<Gs.length;s++){var a=Gs[s];a.blockedOn===t&&(a.blockedOn=null)}}for(mr!==null&&Zi(mr,t),gr!==null&&Zi(gr,t),vr!==null&&Zi(vr,t),Yi.forEach(n),Qi.forEach(n),s=0;s<yr.length;s++)a=yr[s],a.blockedOn===t&&(a.blockedOn=null);for(;0<yr.length&&(s=yr[0],s.blockedOn===null);)tc(s),s.blockedOn===null&&yr.shift()}var mi=B.ReactCurrentBatchConfig,Ks=!0;function wm(t,n,s,a){var u=$e,d=mi.transition;mi.transition=null;try{$e=1,Ta(t,n,s,a)}finally{$e=u,mi.transition=d}}function xm(t,n,s,a){var u=$e,d=mi.transition;mi.transition=null;try{$e=4,Ta(t,n,s,a)}finally{$e=u,mi.transition=d}}function Ta(t,n,s,a){if(Ks){var u=Ca(t,n,s,a);if(u===null)Va(t,n,a,Xs,s),ec(t,a);else if(vm(u,t,n,s,a))a.stopPropagation();else if(ec(t,a),n&4&&-1<gm.indexOf(t)){for(;u!==null;){var d=hs(u);if(d!==null&&Yu(d),d=Ca(t,n,s,a),d===null&&Va(t,n,a,Xs,s),d===u)break;u=d}u!==null&&a.stopPropagation()}else Va(t,n,a,null,s)}}var Xs=null;function Ca(t,n,s,a){if(Xs=null,t=Te(a),t=Gr(t),t!==null)if(n=bn(t),n===null)t=null;else if(s=n.tag,s===13){if(t=Oe(n),t!==null)return t;t=null}else if(s===3){if(n.stateNode.current.memoizedState.isDehydrated)return n.tag===3?n.stateNode.containerInfo:null;t=null}else n!==t&&(t=null);return Xs=t,null}function rc(t){switch(t){case"cancel":case"click":case"close":case"contextmenu":case"copy":case"cut":case"auxclick":case"dblclick":case"dragend":case"dragstart":case"drop":case"focusin":case"focusout":case"input":case"invalid":case"keydown":case"keypress":case"keyup":case"mousedown":case"mouseup":case"paste":case"pause":case"play":case"pointercancel":case"pointerdown":case"pointerup":case"ratechange":case"reset":case"resize":case"seeked":case"submit":case"touchcancel":case"touchend":case"touchstart":case"volumechange":case"change":case"selectionchange":case"textInput":case"compositionstart":case"compositionend":case"compositionupdate":case"beforeblur":case"afterblur":case"beforeinput":case"blur":case"fullscreenchange":case"focus":case"hashchange":case"popstate":case"select":case"selectstart":return 1;case"drag":case"dragenter":case"dragexit":case"dragleave":case"dragover":case"mousemove":case"mouseout":case"mouseover":case"pointermove":case"pointerout":case"pointerover":case"scroll":case"toggle":case"touchmove":case"wheel":case"mouseenter":case"mouseleave":case"pointerenter":case"pointerleave":return 4;case"message":switch(hi()){case Gi:return 1;case fi:return 4;case pi:case _a:return 16;case qn:return 536870912;default:return 16}default:return 16}}var wr=null,Ia=null,Ys=null;function ic(){if(Ys)return Ys;var t,n=Ia,s=n.length,a,u="value"in wr?wr.value:wr.textContent,d=u.length;for(t=0;t<s&&n[t]===u[t];t++);var p=s-t;for(a=1;a<=p&&n[s-a]===u[d-a];a++);return Ys=u.slice(t,1<a?1-a:void 0)}function Qs(t){var n=t.keyCode;return"charCode"in t?(t=t.charCode,t===0&&n===13&&(t=13)):t=n,t===10&&(t=13),32<=t||t===13?t:0}function Js(){return!0}function sc(){return!1}function Zt(t){function n(s,a,u,d,p){this._reactName=s,this._targetInst=u,this.type=a,this.nativeEvent=d,this.target=p,this.currentTarget=null;for(var y in t)t.hasOwnProperty(y)&&(s=t[y],this[y]=s?s(d):d[y]);return this.isDefaultPrevented=(d.defaultPrevented!=null?d.defaultPrevented:d.returnValue===!1)?Js:sc,this.isPropagationStopped=sc,this}return Y(n.prototype,{preventDefault:function(){this.defaultPrevented=!0;var s=this.nativeEvent;s&&(s.preventDefault?s.preventDefault():typeof s.returnValue!="unknown"&&(s.returnValue=!1),this.isDefaultPrevented=Js)},stopPropagation:function(){var s=this.nativeEvent;s&&(s.stopPropagation?s.stopPropagation():typeof s.cancelBubble!="unknown"&&(s.cancelBubble=!0),this.isPropagationStopped=Js)},persist:function(){},isPersistent:Js}),n}var gi={eventPhase:0,bubbles:0,cancelable:0,timeStamp:function(t){return t.timeStamp||Date.now()},defaultPrevented:0,isTrusted:0},Ra=Zt(gi),ts=Y({},gi,{view:0,detail:0}),_m=Zt(ts),Na,Pa,ns,Zs=Y({},ts,{screenX:0,screenY:0,clientX:0,clientY:0,pageX:0,pageY:0,ctrlKey:0,shiftKey:0,altKey:0,metaKey:0,getModifierState:Ma,button:0,buttons:0,relatedTarget:function(t){return t.relatedTarget===void 0?t.fromElement===t.srcElement?t.toElement:t.fromElement:t.relatedTarget},movementX:function(t){return"movementX"in t?t.movementX:(t!==ns&&(ns&&t.type==="mousemove"?(Na=t.screenX-ns.screenX,Pa=t.screenY-ns.screenY):Pa=Na=0,ns=t),Na)},movementY:function(t){return"movementY"in t?t.movementY:Pa}}),oc=Zt(Zs),Em=Y({},Zs,{dataTransfer:0}),Sm=Zt(Em),km=Y({},ts,{relatedTarget:0}),Aa=Zt(km),Tm=Y({},gi,{animationName:0,elapsedTime:0,pseudoElement:0}),Cm=Zt(Tm),Im=Y({},gi,{clipboardData:function(t){return"clipboardData"in t?t.clipboardData:window.clipboardData}}),Rm=Zt(Im),Nm=Y({},gi,{data:0}),ac=Zt(Nm),Pm={Esc:"Escape",Spacebar:" ",Left:"ArrowLeft",Up:"ArrowUp",Right:"ArrowRight",Down:"ArrowDown",Del:"Delete",Win:"OS",Menu:"ContextMenu",Apps:"ContextMenu",Scroll:"ScrollLock",MozPrintableKey:"Unidentified"},Am={8:"Backspace",9:"Tab",12:"Clear",13:"Enter",16:"Shift",17:"Control",18:"Alt",19:"Pause",20:"CapsLock",27:"Escape",32:" ",33:"PageUp",34:"PageDown",35:"End",36:"Home",37:"ArrowLeft",38:"ArrowUp",39:"ArrowRight",40:"ArrowDown",45:"Insert",46:"Delete",112:"F1",113:"F2",114:"F3",115:"F4",116:"F5",117:"F6",118:"F7",119:"F8",120:"F9",121:"F10",122:"F11",123:"F12",144:"NumLock",145:"ScrollLock",224:"Meta"},Mm={Alt:"altKey",Control:"ctrlKey",Meta:"metaKey",Shift:"shiftKey"};function Dm(t){var n=this.nativeEvent;return n.getModifierState?n.getModifierState(t):(t=Mm[t])?!!n[t]:!1}function Ma(){return Dm}var bm=Y({},ts,{key:function(t){if(t.key){var n=Pm[t.key]||t.key;if(n!=="Unidentified")return n}return t.type==="keypress"?(t=Qs(t),t===13?"Enter":String.fromCharCode(t)):t.type==="keydown"||t.type==="keyup"?Am[t.keyCode]||"Unidentified":""},code:0,location:0,ctrlKey:0,shiftKey:0,altKey:0,metaKey:0,repeat:0,locale:0,getModifierState:Ma,charCode:function(t){return t.type==="keypress"?Qs(t):0},keyCode:function(t){return t.type==="keydown"||t.type==="keyup"?t.keyCode:0},which:function(t){return t.type==="keypress"?Qs(t):t.type==="keydown"||t.type==="keyup"?t.keyCode:0}}),Lm=Zt(bm),Om=Y({},Zs,{pointerId:0,width:0,height:0,pressure:0,tangentialPressure:0,tiltX:0,tiltY:0,twist:0,pointerType:0,isPrimary:0}),lc=Zt(Om),Fm=Y({},ts,{touches:0,targetTouches:0,changedTouches:0,altKey:0,metaKey:0,ctrlKey:0,shiftKey:0,getModifierState:Ma}),zm=Zt(Fm),jm=Y({},gi,{propertyName:0,elapsedTime:0,pseudoElement:0}),Um=Zt(jm),Bm=Y({},Zs,{deltaX:function(t){return"deltaX"in t?t.deltaX:"wheelDeltaX"in t?-t.wheelDeltaX:0},deltaY:function(t){return"deltaY"in t?t.deltaY:"wheelDeltaY"in t?-t.wheelDeltaY:"wheelDelta"in t?-t.wheelDelta:0},deltaZ:0,deltaMode:0}),$m=Zt(Bm),Vm=[9,13,27,32],Da=m&&"CompositionEvent"in window,rs=null;m&&"documentMode"in document&&(rs=document.documentMode);var Hm=m&&"TextEvent"in window&&!rs,uc=m&&(!Da||rs&&8<rs&&11>=rs),cc=" ",dc=!1;function hc(t,n){switch(t){case"keyup":return Vm.indexOf(n.keyCode)!==-1;case"keydown":return n.keyCode!==229;case"keypress":case"mousedown":case"focusout":return!0;default:return!1}}function fc(t){return t=t.detail,typeof t=="object"&&"data"in t?t.data:null}var vi=!1;function Wm(t,n){switch(t){case"compositionend":return fc(n);case"keypress":return n.which!==32?null:(dc=!0,cc);case"textInput":return t=n.data,t===cc&&dc?null:t;default:return null}}function Gm(t,n){if(vi)return t==="compositionend"||!Da&&hc(t,n)?(t=ic(),Ys=Ia=wr=null,vi=!1,t):null;switch(t){case"paste":return null;case"keypress":if(!(n.ctrlKey||n.altKey||n.metaKey)||n.ctrlKey&&n.altKey){if(n.char&&1<n.char.length)return n.char;if(n.which)return String.fromCharCode(n.which)}return null;case"compositionend":return uc&&n.locale!=="ko"?null:n.data;default:return null}}var qm={color:!0,date:!0,datetime:!0,"datetime-local":!0,email:!0,month:!0,number:!0,password:!0,range:!0,search:!0,tel:!0,text:!0,time:!0,url:!0,week:!0};function pc(t){var n=t&&t.nodeName&&t.nodeName.toLowerCase();return n==="input"?!!qm[t.type]:n==="textarea"}function mc(t,n,s,a){he(a),n=io(n,"onChange"),0<n.length&&(s=new Ra("onChange","change",null,s,a),t.push({event:s,listeners:n}))}var is=null,ss=null;function Km(t){Dc(t,0)}function eo(t){var n=Ei(t);if(nt(n))return t}function Xm(t,n){if(t==="change")return n}var gc=!1;if(m){var ba;if(m){var La="oninput"in document;if(!La){var vc=document.createElement("div");vc.setAttribute("oninput","return;"),La=typeof vc.oninput=="function"}ba=La}else ba=!1;gc=ba&&(!document.documentMode||9<document.documentMode)}function yc(){is&&(is.detachEvent("onpropertychange",wc),ss=is=null)}function wc(t){if(t.propertyName==="value"&&eo(ss)){var n=[];mc(n,ss,t,Te(t)),ln(Km,n)}}function Ym(t,n,s){t==="focusin"?(yc(),is=n,ss=s,is.attachEvent("onpropertychange",wc)):t==="focusout"&&yc()}function Qm(t){if(t==="selectionchange"||t==="keyup"||t==="keydown")return eo(ss)}function Jm(t,n){if(t==="click")return eo(n)}function Zm(t,n){if(t==="input"||t==="change")return eo(n)}function eg(t,n){return t===n&&(t!==0||1/t===1/n)||t!==t&&n!==n}var _n=typeof Object.is=="function"?Object.is:eg;function os(t,n){if(_n(t,n))return!0;if(typeof t!="object"||t===null||typeof n!="object"||n===null)return!1;var s=Object.keys(t),a=Object.keys(n);if(s.length!==a.length)return!1;for(a=0;a<s.length;a++){var u=s[a];if(!f.call(n,u)||!_n(t[u],n[u]))return!1}return!0}function xc(t){for(;t&&t.firstChild;)t=t.firstChild;return t}function _c(t,n){var s=xc(t);t=0;for(var a;s;){if(s.nodeType===3){if(a=t+s.textContent.length,t<=n&&a>=n)return{node:s,offset:n-t};t=a}e:{for(;s;){if(s.nextSibling){s=s.nextSibling;break e}s=s.parentNode}s=void 0}s=xc(s)}}function Ec(t,n){return t&&n?t===n?!0:t&&t.nodeType===3?!1:n&&n.nodeType===3?Ec(t,n.parentNode):"contains"in t?t.contains(n):t.compareDocumentPosition?!!(t.compareDocumentPosition(n)&16):!1:!1}function Sc(){for(var t=window,n=Qe();n instanceof t.HTMLIFrameElement;){try{var s=typeof n.contentWindow.location.href=="string"}catch{s=!1}if(s)t=n.contentWindow;else break;n=Qe(t.document)}return n}function Oa(t){var n=t&&t.nodeName&&t.nodeName.toLowerCase();return n&&(n==="input"&&(t.type==="text"||t.type==="search"||t.type==="tel"||t.type==="url"||t.type==="password")||n==="textarea"||t.contentEditable==="true")}function tg(t){var n=Sc(),s=t.focusedElem,a=t.selectionRange;if(n!==s&&s&&s.ownerDocument&&Ec(s.ownerDocument.documentElement,s)){if(a!==null&&Oa(s)){if(n=a.start,t=a.end,t===void 0&&(t=n),"selectionStart"in s)s.selectionStart=n,s.selectionEnd=Math.min(t,s.value.length);else if(t=(n=s.ownerDocument||document)&&n.defaultView||window,t.getSelection){t=t.getSelection();var u=s.textContent.length,d=Math.min(a.start,u);a=a.end===void 0?d:Math.min(a.end,u),!t.extend&&d>a&&(u=a,a=d,d=u),u=_c(s,d);var p=_c(s,a);u&&p&&(t.rangeCount!==1||t.anchorNode!==u.node||t.anchorOffset!==u.offset||t.focusNode!==p.node||t.focusOffset!==p.offset)&&(n=n.createRange(),n.setStart(u.node,u.offset),t.removeAllRanges(),d>a?(t.addRange(n),t.extend(p.node,p.offset)):(n.setEnd(p.node,p.offset),t.addRange(n)))}}for(n=[],t=s;t=t.parentNode;)t.nodeType===1&&n.push({element:t,left:t.scrollLeft,top:t.scrollTop});for(typeof s.focus=="function"&&s.focus(),s=0;s<n.length;s++)t=n[s],t.element.scrollLeft=t.left,t.element.scrollTop=t.top}}var ng=m&&"documentMode"in document&&11>=document.documentMode,yi=null,Fa=null,as=null,za=!1;function kc(t,n,s){var a=s.window===s?s.document:s.nodeType===9?s:s.ownerDocument;za||yi==null||yi!==Qe(a)||(a=yi,"selectionStart"in a&&Oa(a)?a={start:a.selectionStart,end:a.selectionEnd}:(a=(a.ownerDocument&&a.ownerDocument.defaultView||window).getSelection(),a={anchorNode:a.anchorNode,anchorOffset:a.anchorOffset,focusNode:a.focusNode,focusOffset:a.focusOffset}),as&&os(as,a)||(as=a,a=io(Fa,"onSelect"),0<a.length&&(n=new Ra("onSelect","select",null,n,s),t.push({event:n,listeners:a}),n.target=yi)))}function to(t,n){var s={};return s[t.toLowerCase()]=n.toLowerCase(),s["Webkit"+t]="webkit"+n,s["Moz"+t]="moz"+n,s}var wi={animationend:to("Animation","AnimationEnd"),animationiteration:to("Animation","AnimationIteration"),animationstart:to("Animation","AnimationStart"),transitionend:to("Transition","TransitionEnd")},ja={},Tc={};m&&(Tc=document.createElement("div").style,"AnimationEvent"in window||(delete wi.animationend.animation,delete wi.animationiteration.animation,delete wi.animationstart.animation),"TransitionEvent"in window||delete wi.transitionend.transition);function no(t){if(ja[t])return ja[t];if(!wi[t])return t;var n=wi[t],s;for(s in n)if(n.hasOwnProperty(s)&&s in Tc)return ja[t]=n[s];return t}var Cc=no("animationend"),Ic=no("animationiteration"),Rc=no("animationstart"),Nc=no("transitionend"),Pc=new Map,Ac="abort auxClick cancel canPlay canPlayThrough click close contextMenu copy cut drag dragEnd dragEnter dragExit dragLeave dragOver dragStart drop durationChange emptied encrypted ended error gotPointerCapture input invalid keyDown keyPress keyUp load loadedData loadedMetadata loadStart lostPointerCapture mouseDown mouseMove mouseOut mouseOver mouseUp paste pause play playing pointerCancel pointerDown pointerMove pointerOut pointerOver pointerUp progress rateChange reset resize seeked seeking stalled submit suspend timeUpdate touchCancel touchEnd touchStart volumeChange scroll toggle touchMove waiting wheel".split(" ");function xr(t,n){Pc.set(t,n),c(n,[t])}for(var Ua=0;Ua<Ac.length;Ua++){var Ba=Ac[Ua],rg=Ba.toLowerCase(),ig=Ba[0].toUpperCase()+Ba.slice(1);xr(rg,"on"+ig)}xr(Cc,"onAnimationEnd"),xr(Ic,"onAnimationIteration"),xr(Rc,"onAnimationStart"),xr("dblclick","onDoubleClick"),xr("focusin","onFocus"),xr("focusout","onBlur"),xr(Nc,"onTransitionEnd"),h("onMouseEnter",["mouseout","mouseover"]),h("onMouseLeave",["mouseout","mouseover"]),h("onPointerEnter",["pointerout","pointerover"]),h("onPointerLeave",["pointerout","pointerover"]),c("onChange","change click focusin focusout input keydown keyup selectionchange".split(" ")),c("onSelect","focusout contextmenu dragend focusin keydown keyup mousedown mouseup selectionchange".split(" ")),c("onBeforeInput",["compositionend","keypress","textInput","paste"]),c("onCompositionEnd","compositionend focusout keydown keypress keyup mousedown".split(" ")),c("onCompositionStart","compositionstart focusout keydown keypress keyup mousedown".split(" ")),c("onCompositionUpdate","compositionupdate focusout keydown keypress keyup mousedown".split(" "));var ls="abort canplay canplaythrough durationchange emptied encrypted ended error loadeddata loadedmetadata loadstart pause play playing progress ratechange resize seeked seeking stalled suspend timeupdate volumechange waiting".split(" "),sg=new Set("cancel close invalid load scroll toggle".split(" ").concat(ls));function Mc(t,n,s){var a=t.type||"unknown-event";t.currentTarget=s,Hs(a,n,void 0,t),t.currentTarget=null}function Dc(t,n){n=(n&4)!==0;for(var s=0;s<t.length;s++){var a=t[s],u=a.event;a=a.listeners;e:{var d=void 0;if(n)for(var p=a.length-1;0<=p;p--){var y=a[p],_=y.instance,M=y.currentTarget;if(y=y.listener,_!==d&&u.isPropagationStopped())break e;Mc(u,y,M),d=_}else for(p=0;p<a.length;p++){if(y=a[p],_=y.instance,M=y.currentTarget,y=y.listener,_!==d&&u.isPropagationStopped())break e;Mc(u,y,M),d=_}}}if(St)throw t=Gn,St=!1,Gn=null,t}function Ke(t,n){var s=n[Xa];s===void 0&&(s=n[Xa]=new Set);var a=t+"__bubble";s.has(a)||(bc(n,t,2,!1),s.add(a))}function $a(t,n,s){var a=0;n&&(a|=4),bc(s,t,a,n)}var ro="_reactListening"+Math.random().toString(36).slice(2);function us(t){if(!t[ro]){t[ro]=!0,o.forEach(function(s){s!=="selectionchange"&&(sg.has(s)||$a(s,!1,t),$a(s,!0,t))});var n=t.nodeType===9?t:t.ownerDocument;n===null||n[ro]||(n[ro]=!0,$a("selectionchange",!1,n))}}function bc(t,n,s,a){switch(rc(n)){case 1:var u=wm;break;case 4:u=xm;break;default:u=Ta}s=u.bind(null,n,s,t),u=void 0,!wt||n!=="touchstart"&&n!=="touchmove"&&n!=="wheel"||(u=!0),a?u!==void 0?t.addEventListener(n,s,{capture:!0,passive:u}):t.addEventListener(n,s,!0):u!==void 0?t.addEventListener(n,s,{passive:u}):t.addEventListener(n,s,!1)}function Va(t,n,s,a,u){var d=a;if((n&1)===0&&(n&2)===0&&a!==null)e:for(;;){if(a===null)return;var p=a.tag;if(p===3||p===4){var y=a.stateNode.containerInfo;if(y===u||y.nodeType===8&&y.parentNode===u)break;if(p===4)for(p=a.return;p!==null;){var _=p.tag;if((_===3||_===4)&&(_=p.stateNode.containerInfo,_===u||_.nodeType===8&&_.parentNode===u))return;p=p.return}for(;y!==null;){if(p=Gr(y),p===null)return;if(_=p.tag,_===5||_===6){a=d=p;continue e}y=y.parentNode}}a=a.return}ln(function(){var M=d,U=Te(s),$=[];e:{var z=Pc.get(t);if(z!==void 0){var Z=Ra,ie=t;switch(t){case"keypress":if(Qs(s)===0)break e;case"keydown":case"keyup":Z=Lm;break;case"focusin":ie="focus",Z=Aa;break;case"focusout":ie="blur",Z=Aa;break;case"beforeblur":case"afterblur":Z=Aa;break;case"click":if(s.button===2)break e;case"auxclick":case"dblclick":case"mousedown":case"mousemove":case"mouseup":case"mouseout":case"mouseover":case"contextmenu":Z=oc;break;case"drag":case"dragend":case"dragenter":case"dragexit":case"dragleave":case"dragover":case"dragstart":case"drop":Z=Sm;break;case"touchcancel":case"touchend":case"touchmove":case"touchstart":Z=zm;break;case Cc:case Ic:case Rc:Z=Cm;break;case Nc:Z=Um;break;case"scroll":Z=_m;break;case"wheel":Z=$m;break;case"copy":case"cut":case"paste":Z=Rm;break;case"gotpointercapture":case"lostpointercapture":case"pointercancel":case"pointerdown":case"pointermove":case"pointerout":case"pointerover":case"pointerup":Z=lc}var ae=(n&4)!==0,st=!ae&&t==="scroll",I=ae?z!==null?z+"Capture":null:z;ae=[];for(var k=M,N;k!==null;){N=k;var X=N.stateNode;if(N.tag===5&&X!==null&&(N=X,I!==null&&(X=lt(k,I),X!=null&&ae.push(cs(k,X,N)))),st)break;k=k.return}0<ae.length&&(z=new Z(z,ie,null,s,U),$.push({event:z,listeners:ae}))}}if((n&7)===0){e:{if(z=t==="mouseover"||t==="pointerover",Z=t==="mouseout"||t==="pointerout",z&&s!==oe&&(ie=s.relatedTarget||s.fromElement)&&(Gr(ie)||ie[Xn]))break e;if((Z||z)&&(z=U.window===U?U:(z=U.ownerDocument)?z.defaultView||z.parentWindow:window,Z?(ie=s.relatedTarget||s.toElement,Z=M,ie=ie?Gr(ie):null,ie!==null&&(st=bn(ie),ie!==st||ie.tag!==5&&ie.tag!==6)&&(ie=null)):(Z=null,ie=M),Z!==ie)){if(ae=oc,X="onMouseLeave",I="onMouseEnter",k="mouse",(t==="pointerout"||t==="pointerover")&&(ae=lc,X="onPointerLeave",I="onPointerEnter",k="pointer"),st=Z==null?z:Ei(Z),N=ie==null?z:Ei(ie),z=new ae(X,k+"leave",Z,s,U),z.target=st,z.relatedTarget=N,X=null,Gr(U)===M&&(ae=new ae(I,k+"enter",ie,s,U),ae.target=N,ae.relatedTarget=st,X=ae),st=X,Z&&ie)t:{for(ae=Z,I=ie,k=0,N=ae;N;N=xi(N))k++;for(N=0,X=I;X;X=xi(X))N++;for(;0<k-N;)ae=xi(ae),k--;for(;0<N-k;)I=xi(I),N--;for(;k--;){if(ae===I||I!==null&&ae===I.alternate)break t;ae=xi(ae),I=xi(I)}ae=null}else ae=null;Z!==null&&Lc($,z,Z,ae,!1),ie!==null&&st!==null&&Lc($,st,ie,ae,!0)}}e:{if(z=M?Ei(M):window,Z=z.nodeName&&z.nodeName.toLowerCase(),Z==="select"||Z==="input"&&z.type==="file")var le=Xm;else if(pc(z))if(gc)le=Zm;else{le=Qm;var ge=Ym}else(Z=z.nodeName)&&Z.toLowerCase()==="input"&&(z.type==="checkbox"||z.type==="radio")&&(le=Jm);if(le&&(le=le(t,M))){mc($,le,s,U);break e}ge&&ge(t,z,M),t==="focusout"&&(ge=z._wrapperState)&&ge.controlled&&z.type==="number"&&Hn(z,"number",z.value)}switch(ge=M?Ei(M):window,t){case"focusin":(pc(ge)||ge.contentEditable==="true")&&(yi=ge,Fa=M,as=null);break;case"focusout":as=Fa=yi=null;break;case"mousedown":za=!0;break;case"contextmenu":case"mouseup":case"dragend":za=!1,kc($,s,U);break;case"selectionchange":if(ng)break;case"keydown":case"keyup":kc($,s,U)}var ve;if(Da)e:{switch(t){case"compositionstart":var Ie="onCompositionStart";break e;case"compositionend":Ie="onCompositionEnd";break e;case"compositionupdate":Ie="onCompositionUpdate";break e}Ie=void 0}else vi?hc(t,s)&&(Ie="onCompositionEnd"):t==="keydown"&&s.keyCode===229&&(Ie="onCompositionStart");Ie&&(uc&&s.locale!=="ko"&&(vi||Ie!=="onCompositionStart"?Ie==="onCompositionEnd"&&vi&&(ve=ic()):(wr=U,Ia="value"in wr?wr.value:wr.textContent,vi=!0)),ge=io(M,Ie),0<ge.length&&(Ie=new ac(Ie,t,null,s,U),$.push({event:Ie,listeners:ge}),ve?Ie.data=ve:(ve=fc(s),ve!==null&&(Ie.data=ve)))),(ve=Hm?Wm(t,s):Gm(t,s))&&(M=io(M,"onBeforeInput"),0<M.length&&(U=new ac("onBeforeInput","beforeinput",null,s,U),$.push({event:U,listeners:M}),U.data=ve))}Dc($,n)})}function cs(t,n,s){return{instance:t,listener:n,currentTarget:s}}function io(t,n){for(var s=n+"Capture",a=[];t!==null;){var u=t,d=u.stateNode;u.tag===5&&d!==null&&(u=d,d=lt(t,s),d!=null&&a.unshift(cs(t,d,u)),d=lt(t,n),d!=null&&a.push(cs(t,d,u))),t=t.return}return a}function xi(t){if(t===null)return null;do t=t.return;while(t&&t.tag!==5);return t||null}function Lc(t,n,s,a,u){for(var d=n._reactName,p=[];s!==null&&s!==a;){var y=s,_=y.alternate,M=y.stateNode;if(_!==null&&_===a)break;y.tag===5&&M!==null&&(y=M,u?(_=lt(s,d),_!=null&&p.unshift(cs(s,_,y))):u||(_=lt(s,d),_!=null&&p.push(cs(s,_,y)))),s=s.return}p.length!==0&&t.push({event:n,listeners:p})}var og=/\r\n?/g,ag=/\u0000|\uFFFD/g;function Oc(t){return(typeof t=="string"?t:""+t).replace(og,`
`).replace(ag,"")}function so(t,n,s){if(n=Oc(n),Oc(t)!==n&&s)throw Error(r(425))}function oo(){}var Ha=null,Wa=null;function Ga(t,n){return t==="textarea"||t==="noscript"||typeof n.children=="string"||typeof n.children=="number"||typeof n.dangerouslySetInnerHTML=="object"&&n.dangerouslySetInnerHTML!==null&&n.dangerouslySetInnerHTML.__html!=null}var qa=typeof setTimeout=="function"?setTimeout:void 0,lg=typeof clearTimeout=="function"?clearTimeout:void 0,Fc=typeof Promise=="function"?Promise:void 0,ug=typeof queueMicrotask=="function"?queueMicrotask:typeof Fc<"u"?function(t){return Fc.resolve(null).then(t).catch(cg)}:qa;function cg(t){setTimeout(function(){throw t})}function Ka(t,n){var s=n,a=0;do{var u=s.nextSibling;if(t.removeChild(s),u&&u.nodeType===8)if(s=u.data,s==="/$"){if(a===0){t.removeChild(u),es(n);return}a--}else s!=="$"&&s!=="$?"&&s!=="$!"||a++;s=u}while(s);es(n)}function _r(t){for(;t!=null;t=t.nextSibling){var n=t.nodeType;if(n===1||n===3)break;if(n===8){if(n=t.data,n==="$"||n==="$!"||n==="$?")break;if(n==="/$")return null}}return t}function zc(t){t=t.previousSibling;for(var n=0;t;){if(t.nodeType===8){var s=t.data;if(s==="$"||s==="$!"||s==="$?"){if(n===0)return t;n--}else s==="/$"&&n++}t=t.previousSibling}return null}var _i=Math.random().toString(36).slice(2),Ln="__reactFiber$"+_i,ds="__reactProps$"+_i,Xn="__reactContainer$"+_i,Xa="__reactEvents$"+_i,dg="__reactListeners$"+_i,hg="__reactHandles$"+_i;function Gr(t){var n=t[Ln];if(n)return n;for(var s=t.parentNode;s;){if(n=s[Xn]||s[Ln]){if(s=n.alternate,n.child!==null||s!==null&&s.child!==null)for(t=zc(t);t!==null;){if(s=t[Ln])return s;t=zc(t)}return n}t=s,s=t.parentNode}return null}function hs(t){return t=t[Ln]||t[Xn],!t||t.tag!==5&&t.tag!==6&&t.tag!==13&&t.tag!==3?null:t}function Ei(t){if(t.tag===5||t.tag===6)return t.stateNode;throw Error(r(33))}function ao(t){return t[ds]||null}var Ya=[],Si=-1;function Er(t){return{current:t}}function Xe(t){0>Si||(t.current=Ya[Si],Ya[Si]=null,Si--)}function qe(t,n){Si++,Ya[Si]=t.current,t.current=n}var Sr={},Tt=Er(Sr),Bt=Er(!1),qr=Sr;function ki(t,n){var s=t.type.contextTypes;if(!s)return Sr;var a=t.stateNode;if(a&&a.__reactInternalMemoizedUnmaskedChildContext===n)return a.__reactInternalMemoizedMaskedChildContext;var u={},d;for(d in s)u[d]=n[d];return a&&(t=t.stateNode,t.__reactInternalMemoizedUnmaskedChildContext=n,t.__reactInternalMemoizedMaskedChildContext=u),u}function $t(t){return t=t.childContextTypes,t!=null}function lo(){Xe(Bt),Xe(Tt)}function jc(t,n,s){if(Tt.current!==Sr)throw Error(r(168));qe(Tt,n),qe(Bt,s)}function Uc(t,n,s){var a=t.stateNode;if(n=n.childContextTypes,typeof a.getChildContext!="function")return s;a=a.getChildContext();for(var u in a)if(!(u in n))throw Error(r(108,Me(t)||"Unknown",u));return Y({},s,a)}function uo(t){return t=(t=t.stateNode)&&t.__reactInternalMemoizedMergedChildContext||Sr,qr=Tt.current,qe(Tt,t),qe(Bt,Bt.current),!0}function Bc(t,n,s){var a=t.stateNode;if(!a)throw Error(r(169));s?(t=Uc(t,n,qr),a.__reactInternalMemoizedMergedChildContext=t,Xe(Bt),Xe(Tt),qe(Tt,t)):Xe(Bt),qe(Bt,s)}var Yn=null,co=!1,Qa=!1;function $c(t){Yn===null?Yn=[t]:Yn.push(t)}function fg(t){co=!0,$c(t)}function kr(){if(!Qa&&Yn!==null){Qa=!0;var t=0,n=$e;try{var s=Yn;for($e=1;t<s.length;t++){var a=s[t];do a=a(!0);while(a!==null)}Yn=null,co=!1}catch(u){throw Yn!==null&&(Yn=Yn.slice(t+1)),Yt(Gi,kr),u}finally{$e=n,Qa=!1}}return null}var Ti=[],Ci=0,ho=null,fo=0,dn=[],hn=0,Kr=null,Qn=1,Jn="";function Xr(t,n){Ti[Ci++]=fo,Ti[Ci++]=ho,ho=t,fo=n}function Vc(t,n,s){dn[hn++]=Qn,dn[hn++]=Jn,dn[hn++]=Kr,Kr=t;var a=Qn;t=Jn;var u=32-jt(a)-1;a&=~(1<<u),s+=1;var d=32-jt(n)+u;if(30<d){var p=u-u%5;d=(a&(1<<p)-1).toString(32),a>>=p,u-=p,Qn=1<<32-jt(n)+u|s<<u|a,Jn=d+t}else Qn=1<<d|s<<u|a,Jn=t}function Ja(t){t.return!==null&&(Xr(t,1),Vc(t,1,0))}function Za(t){for(;t===ho;)ho=Ti[--Ci],Ti[Ci]=null,fo=Ti[--Ci],Ti[Ci]=null;for(;t===Kr;)Kr=dn[--hn],dn[hn]=null,Jn=dn[--hn],dn[hn]=null,Qn=dn[--hn],dn[hn]=null}var en=null,tn=null,Je=!1,En=null;function Hc(t,n){var s=gn(5,null,null,0);s.elementType="DELETED",s.stateNode=n,s.return=t,n=t.deletions,n===null?(t.deletions=[s],t.flags|=16):n.push(s)}function Wc(t,n){switch(t.tag){case 5:var s=t.type;return n=n.nodeType!==1||s.toLowerCase()!==n.nodeName.toLowerCase()?null:n,n!==null?(t.stateNode=n,en=t,tn=_r(n.firstChild),!0):!1;case 6:return n=t.pendingProps===""||n.nodeType!==3?null:n,n!==null?(t.stateNode=n,en=t,tn=null,!0):!1;case 13:return n=n.nodeType!==8?null:n,n!==null?(s=Kr!==null?{id:Qn,overflow:Jn}:null,t.memoizedState={dehydrated:n,treeContext:s,retryLane:1073741824},s=gn(18,null,null,0),s.stateNode=n,s.return=t,t.child=s,en=t,tn=null,!0):!1;default:return!1}}function el(t){return(t.mode&1)!==0&&(t.flags&128)===0}function tl(t){if(Je){var n=tn;if(n){var s=n;if(!Wc(t,n)){if(el(t))throw Error(r(418));n=_r(s.nextSibling);var a=en;n&&Wc(t,n)?Hc(a,s):(t.flags=t.flags&-4097|2,Je=!1,en=t)}}else{if(el(t))throw Error(r(418));t.flags=t.flags&-4097|2,Je=!1,en=t}}}function Gc(t){for(t=t.return;t!==null&&t.tag!==5&&t.tag!==3&&t.tag!==13;)t=t.return;en=t}function po(t){if(t!==en)return!1;if(!Je)return Gc(t),Je=!0,!1;var n;if((n=t.tag!==3)&&!(n=t.tag!==5)&&(n=t.type,n=n!=="head"&&n!=="body"&&!Ga(t.type,t.memoizedProps)),n&&(n=tn)){if(el(t))throw qc(),Error(r(418));for(;n;)Hc(t,n),n=_r(n.nextSibling)}if(Gc(t),t.tag===13){if(t=t.memoizedState,t=t!==null?t.dehydrated:null,!t)throw Error(r(317));e:{for(t=t.nextSibling,n=0;t;){if(t.nodeType===8){var s=t.data;if(s==="/$"){if(n===0){tn=_r(t.nextSibling);break e}n--}else s!=="$"&&s!=="$!"&&s!=="$?"||n++}t=t.nextSibling}tn=null}}else tn=en?_r(t.stateNode.nextSibling):null;return!0}function qc(){for(var t=tn;t;)t=_r(t.nextSibling)}function Ii(){tn=en=null,Je=!1}function nl(t){En===null?En=[t]:En.push(t)}var pg=B.ReactCurrentBatchConfig;function fs(t,n,s){if(t=s.ref,t!==null&&typeof t!="function"&&typeof t!="object"){if(s._owner){if(s=s._owner,s){if(s.tag!==1)throw Error(r(309));var a=s.stateNode}if(!a)throw Error(r(147,t));var u=a,d=""+t;return n!==null&&n.ref!==null&&typeof n.ref=="function"&&n.ref._stringRef===d?n.ref:(n=function(p){var y=u.refs;p===null?delete y[d]:y[d]=p},n._stringRef=d,n)}if(typeof t!="string")throw Error(r(284));if(!s._owner)throw Error(r(290,t))}return t}function mo(t,n){throw t=Object.prototype.toString.call(n),Error(r(31,t==="[object Object]"?"object with keys {"+Object.keys(n).join(", ")+"}":t))}function Kc(t){var n=t._init;return n(t._payload)}function Xc(t){function n(I,k){if(t){var N=I.deletions;N===null?(I.deletions=[k],I.flags|=16):N.push(k)}}function s(I,k){if(!t)return null;for(;k!==null;)n(I,k),k=k.sibling;return null}function a(I,k){for(I=new Map;k!==null;)k.key!==null?I.set(k.key,k):I.set(k.index,k),k=k.sibling;return I}function u(I,k){return I=Mr(I,k),I.index=0,I.sibling=null,I}function d(I,k,N){return I.index=N,t?(N=I.alternate,N!==null?(N=N.index,N<k?(I.flags|=2,k):N):(I.flags|=2,k)):(I.flags|=1048576,k)}function p(I){return t&&I.alternate===null&&(I.flags|=2),I}function y(I,k,N,X){return k===null||k.tag!==6?(k=ql(N,I.mode,X),k.return=I,k):(k=u(k,N),k.return=I,k)}function _(I,k,N,X){var le=N.type;return le===pe?U(I,k,N.props.children,X,N.key):k!==null&&(k.elementType===le||typeof le=="object"&&le!==null&&le.$$typeof===Pe&&Kc(le)===k.type)?(X=u(k,N.props),X.ref=fs(I,k,N),X.return=I,X):(X=jo(N.type,N.key,N.props,null,I.mode,X),X.ref=fs(I,k,N),X.return=I,X)}function M(I,k,N,X){return k===null||k.tag!==4||k.stateNode.containerInfo!==N.containerInfo||k.stateNode.implementation!==N.implementation?(k=Kl(N,I.mode,X),k.return=I,k):(k=u(k,N.children||[]),k.return=I,k)}function U(I,k,N,X,le){return k===null||k.tag!==7?(k=ri(N,I.mode,X,le),k.return=I,k):(k=u(k,N),k.return=I,k)}function $(I,k,N){if(typeof k=="string"&&k!==""||typeof k=="number")return k=ql(""+k,I.mode,N),k.return=I,k;if(typeof k=="object"&&k!==null){switch(k.$$typeof){case W:return N=jo(k.type,k.key,k.props,null,I.mode,N),N.ref=fs(I,null,k),N.return=I,N;case Q:return k=Kl(k,I.mode,N),k.return=I,k;case Pe:var X=k._init;return $(I,X(k._payload),N)}if(on(k)||ee(k))return k=ri(k,I.mode,N,null),k.return=I,k;mo(I,k)}return null}function z(I,k,N,X){var le=k!==null?k.key:null;if(typeof N=="string"&&N!==""||typeof N=="number")return le!==null?null:y(I,k,""+N,X);if(typeof N=="object"&&N!==null){switch(N.$$typeof){case W:return N.key===le?_(I,k,N,X):null;case Q:return N.key===le?M(I,k,N,X):null;case Pe:return le=N._init,z(I,k,le(N._payload),X)}if(on(N)||ee(N))return le!==null?null:U(I,k,N,X,null);mo(I,N)}return null}function Z(I,k,N,X,le){if(typeof X=="string"&&X!==""||typeof X=="number")return I=I.get(N)||null,y(k,I,""+X,le);if(typeof X=="object"&&X!==null){switch(X.$$typeof){case W:return I=I.get(X.key===null?N:X.key)||null,_(k,I,X,le);case Q:return I=I.get(X.key===null?N:X.key)||null,M(k,I,X,le);case Pe:var ge=X._init;return Z(I,k,N,ge(X._payload),le)}if(on(X)||ee(X))return I=I.get(N)||null,U(k,I,X,le,null);mo(k,X)}return null}function ie(I,k,N,X){for(var le=null,ge=null,ve=k,Ie=k=0,gt=null;ve!==null&&Ie<N.length;Ie++){ve.index>Ie?(gt=ve,ve=null):gt=ve.sibling;var je=z(I,ve,N[Ie],X);if(je===null){ve===null&&(ve=gt);break}t&&ve&&je.alternate===null&&n(I,ve),k=d(je,k,Ie),ge===null?le=je:ge.sibling=je,ge=je,ve=gt}if(Ie===N.length)return s(I,ve),Je&&Xr(I,Ie),le;if(ve===null){for(;Ie<N.length;Ie++)ve=$(I,N[Ie],X),ve!==null&&(k=d(ve,k,Ie),ge===null?le=ve:ge.sibling=ve,ge=ve);return Je&&Xr(I,Ie),le}for(ve=a(I,ve);Ie<N.length;Ie++)gt=Z(ve,I,Ie,N[Ie],X),gt!==null&&(t&&gt.alternate!==null&&ve.delete(gt.key===null?Ie:gt.key),k=d(gt,k,Ie),ge===null?le=gt:ge.sibling=gt,ge=gt);return t&&ve.forEach(function(Dr){return n(I,Dr)}),Je&&Xr(I,Ie),le}function ae(I,k,N,X){var le=ee(N);if(typeof le!="function")throw Error(r(150));if(N=le.call(N),N==null)throw Error(r(151));for(var ge=le=null,ve=k,Ie=k=0,gt=null,je=N.next();ve!==null&&!je.done;Ie++,je=N.next()){ve.index>Ie?(gt=ve,ve=null):gt=ve.sibling;var Dr=z(I,ve,je.value,X);if(Dr===null){ve===null&&(ve=gt);break}t&&ve&&Dr.alternate===null&&n(I,ve),k=d(Dr,k,Ie),ge===null?le=Dr:ge.sibling=Dr,ge=Dr,ve=gt}if(je.done)return s(I,ve),Je&&Xr(I,Ie),le;if(ve===null){for(;!je.done;Ie++,je=N.next())je=$(I,je.value,X),je!==null&&(k=d(je,k,Ie),ge===null?le=je:ge.sibling=je,ge=je);return Je&&Xr(I,Ie),le}for(ve=a(I,ve);!je.done;Ie++,je=N.next())je=Z(ve,I,Ie,je.value,X),je!==null&&(t&&je.alternate!==null&&ve.delete(je.key===null?Ie:je.key),k=d(je,k,Ie),ge===null?le=je:ge.sibling=je,ge=je);return t&&ve.forEach(function(qg){return n(I,qg)}),Je&&Xr(I,Ie),le}function st(I,k,N,X){if(typeof N=="object"&&N!==null&&N.type===pe&&N.key===null&&(N=N.props.children),typeof N=="object"&&N!==null){switch(N.$$typeof){case W:e:{for(var le=N.key,ge=k;ge!==null;){if(ge.key===le){if(le=N.type,le===pe){if(ge.tag===7){s(I,ge.sibling),k=u(ge,N.props.children),k.return=I,I=k;break e}}else if(ge.elementType===le||typeof le=="object"&&le!==null&&le.$$typeof===Pe&&Kc(le)===ge.type){s(I,ge.sibling),k=u(ge,N.props),k.ref=fs(I,ge,N),k.return=I,I=k;break e}s(I,ge);break}else n(I,ge);ge=ge.sibling}N.type===pe?(k=ri(N.props.children,I.mode,X,N.key),k.return=I,I=k):(X=jo(N.type,N.key,N.props,null,I.mode,X),X.ref=fs(I,k,N),X.return=I,I=X)}return p(I);case Q:e:{for(ge=N.key;k!==null;){if(k.key===ge)if(k.tag===4&&k.stateNode.containerInfo===N.containerInfo&&k.stateNode.implementation===N.implementation){s(I,k.sibling),k=u(k,N.children||[]),k.return=I,I=k;break e}else{s(I,k);break}else n(I,k);k=k.sibling}k=Kl(N,I.mode,X),k.return=I,I=k}return p(I);case Pe:return ge=N._init,st(I,k,ge(N._payload),X)}if(on(N))return ie(I,k,N,X);if(ee(N))return ae(I,k,N,X);mo(I,N)}return typeof N=="string"&&N!==""||typeof N=="number"?(N=""+N,k!==null&&k.tag===6?(s(I,k.sibling),k=u(k,N),k.return=I,I=k):(s(I,k),k=ql(N,I.mode,X),k.return=I,I=k),p(I)):s(I,k)}return st}var Ri=Xc(!0),Yc=Xc(!1),go=Er(null),vo=null,Ni=null,rl=null;function il(){rl=Ni=vo=null}function sl(t){var n=go.current;Xe(go),t._currentValue=n}function ol(t,n,s){for(;t!==null;){var a=t.alternate;if((t.childLanes&n)!==n?(t.childLanes|=n,a!==null&&(a.childLanes|=n)):a!==null&&(a.childLanes&n)!==n&&(a.childLanes|=n),t===s)break;t=t.return}}function Pi(t,n){vo=t,rl=Ni=null,t=t.dependencies,t!==null&&t.firstContext!==null&&((t.lanes&n)!==0&&(Vt=!0),t.firstContext=null)}function fn(t){var n=t._currentValue;if(rl!==t)if(t={context:t,memoizedValue:n,next:null},Ni===null){if(vo===null)throw Error(r(308));Ni=t,vo.dependencies={lanes:0,firstContext:t}}else Ni=Ni.next=t;return n}var Yr=null;function al(t){Yr===null?Yr=[t]:Yr.push(t)}function Qc(t,n,s,a){var u=n.interleaved;return u===null?(s.next=s,al(n)):(s.next=u.next,u.next=s),n.interleaved=s,Zn(t,a)}function Zn(t,n){t.lanes|=n;var s=t.alternate;for(s!==null&&(s.lanes|=n),s=t,t=t.return;t!==null;)t.childLanes|=n,s=t.alternate,s!==null&&(s.childLanes|=n),s=t,t=t.return;return s.tag===3?s.stateNode:null}var Tr=!1;function ll(t){t.updateQueue={baseState:t.memoizedState,firstBaseUpdate:null,lastBaseUpdate:null,shared:{pending:null,interleaved:null,lanes:0},effects:null}}function Jc(t,n){t=t.updateQueue,n.updateQueue===t&&(n.updateQueue={baseState:t.baseState,firstBaseUpdate:t.firstBaseUpdate,lastBaseUpdate:t.lastBaseUpdate,shared:t.shared,effects:t.effects})}function er(t,n){return{eventTime:t,lane:n,tag:0,payload:null,callback:null,next:null}}function Cr(t,n,s){var a=t.updateQueue;if(a===null)return null;if(a=a.shared,(ze&2)!==0){var u=a.pending;return u===null?n.next=n:(n.next=u.next,u.next=n),a.pending=n,Zn(t,s)}return u=a.interleaved,u===null?(n.next=n,al(a)):(n.next=u.next,u.next=n),a.interleaved=n,Zn(t,s)}function yo(t,n,s){if(n=n.updateQueue,n!==null&&(n=n.shared,(s&4194240)!==0)){var a=n.lanes;a&=t.pendingLanes,s|=a,n.lanes=s,xn(t,s)}}function Zc(t,n){var s=t.updateQueue,a=t.alternate;if(a!==null&&(a=a.updateQueue,s===a)){var u=null,d=null;if(s=s.firstBaseUpdate,s!==null){do{var p={eventTime:s.eventTime,lane:s.lane,tag:s.tag,payload:s.payload,callback:s.callback,next:null};d===null?u=d=p:d=d.next=p,s=s.next}while(s!==null);d===null?u=d=n:d=d.next=n}else u=d=n;s={baseState:a.baseState,firstBaseUpdate:u,lastBaseUpdate:d,shared:a.shared,effects:a.effects},t.updateQueue=s;return}t=s.lastBaseUpdate,t===null?s.firstBaseUpdate=n:t.next=n,s.lastBaseUpdate=n}function wo(t,n,s,a){var u=t.updateQueue;Tr=!1;var d=u.firstBaseUpdate,p=u.lastBaseUpdate,y=u.shared.pending;if(y!==null){u.shared.pending=null;var _=y,M=_.next;_.next=null,p===null?d=M:p.next=M,p=_;var U=t.alternate;U!==null&&(U=U.updateQueue,y=U.lastBaseUpdate,y!==p&&(y===null?U.firstBaseUpdate=M:y.next=M,U.lastBaseUpdate=_))}if(d!==null){var $=u.baseState;p=0,U=M=_=null,y=d;do{var z=y.lane,Z=y.eventTime;if((a&z)===z){U!==null&&(U=U.next={eventTime:Z,lane:0,tag:y.tag,payload:y.payload,callback:y.callback,next:null});e:{var ie=t,ae=y;switch(z=n,Z=s,ae.tag){case 1:if(ie=ae.payload,typeof ie=="function"){$=ie.call(Z,$,z);break e}$=ie;break e;case 3:ie.flags=ie.flags&-65537|128;case 0:if(ie=ae.payload,z=typeof ie=="function"?ie.call(Z,$,z):ie,z==null)break e;$=Y({},$,z);break e;case 2:Tr=!0}}y.callback!==null&&y.lane!==0&&(t.flags|=64,z=u.effects,z===null?u.effects=[y]:z.push(y))}else Z={eventTime:Z,lane:z,tag:y.tag,payload:y.payload,callback:y.callback,next:null},U===null?(M=U=Z,_=$):U=U.next=Z,p|=z;if(y=y.next,y===null){if(y=u.shared.pending,y===null)break;z=y,y=z.next,z.next=null,u.lastBaseUpdate=z,u.shared.pending=null}}while(!0);if(U===null&&(_=$),u.baseState=_,u.firstBaseUpdate=M,u.lastBaseUpdate=U,n=u.shared.interleaved,n!==null){u=n;do p|=u.lane,u=u.next;while(u!==n)}else d===null&&(u.shared.lanes=0);Zr|=p,t.lanes=p,t.memoizedState=$}}function ed(t,n,s){if(t=n.effects,n.effects=null,t!==null)for(n=0;n<t.length;n++){var a=t[n],u=a.callback;if(u!==null){if(a.callback=null,a=s,typeof u!="function")throw Error(r(191,u));u.call(a)}}}var ps={},On=Er(ps),ms=Er(ps),gs=Er(ps);function Qr(t){if(t===ps)throw Error(r(174));return t}function ul(t,n){switch(qe(gs,n),qe(ms,t),qe(On,ps),t=n.nodeType,t){case 9:case 11:n=(n=n.documentElement)?n.namespaceURI:ft(null,"");break;default:t=t===8?n.parentNode:n,n=t.namespaceURI||null,t=t.tagName,n=ft(n,t)}Xe(On),qe(On,n)}function Ai(){Xe(On),Xe(ms),Xe(gs)}function td(t){Qr(gs.current);var n=Qr(On.current),s=ft(n,t.type);n!==s&&(qe(ms,t),qe(On,s))}function cl(t){ms.current===t&&(Xe(On),Xe(ms))}var Ze=Er(0);function xo(t){for(var n=t;n!==null;){if(n.tag===13){var s=n.memoizedState;if(s!==null&&(s=s.dehydrated,s===null||s.data==="$?"||s.data==="$!"))return n}else if(n.tag===19&&n.memoizedProps.revealOrder!==void 0){if((n.flags&128)!==0)return n}else if(n.child!==null){n.child.return=n,n=n.child;continue}if(n===t)break;for(;n.sibling===null;){if(n.return===null||n.return===t)return null;n=n.return}n.sibling.return=n.return,n=n.sibling}return null}var dl=[];function hl(){for(var t=0;t<dl.length;t++)dl[t]._workInProgressVersionPrimary=null;dl.length=0}var _o=B.ReactCurrentDispatcher,fl=B.ReactCurrentBatchConfig,Jr=0,et=null,dt=null,pt=null,Eo=!1,vs=!1,ys=0,mg=0;function Ct(){throw Error(r(321))}function pl(t,n){if(n===null)return!1;for(var s=0;s<n.length&&s<t.length;s++)if(!_n(t[s],n[s]))return!1;return!0}function ml(t,n,s,a,u,d){if(Jr=d,et=n,n.memoizedState=null,n.updateQueue=null,n.lanes=0,_o.current=t===null||t.memoizedState===null?wg:xg,t=s(a,u),vs){d=0;do{if(vs=!1,ys=0,25<=d)throw Error(r(301));d+=1,pt=dt=null,n.updateQueue=null,_o.current=_g,t=s(a,u)}while(vs)}if(_o.current=To,n=dt!==null&&dt.next!==null,Jr=0,pt=dt=et=null,Eo=!1,n)throw Error(r(300));return t}function gl(){var t=ys!==0;return ys=0,t}function Fn(){var t={memoizedState:null,baseState:null,baseQueue:null,queue:null,next:null};return pt===null?et.memoizedState=pt=t:pt=pt.next=t,pt}function pn(){if(dt===null){var t=et.alternate;t=t!==null?t.memoizedState:null}else t=dt.next;var n=pt===null?et.memoizedState:pt.next;if(n!==null)pt=n,dt=t;else{if(t===null)throw Error(r(310));dt=t,t={memoizedState:dt.memoizedState,baseState:dt.baseState,baseQueue:dt.baseQueue,queue:dt.queue,next:null},pt===null?et.memoizedState=pt=t:pt=pt.next=t}return pt}function ws(t,n){return typeof n=="function"?n(t):n}function vl(t){var n=pn(),s=n.queue;if(s===null)throw Error(r(311));s.lastRenderedReducer=t;var a=dt,u=a.baseQueue,d=s.pending;if(d!==null){if(u!==null){var p=u.next;u.next=d.next,d.next=p}a.baseQueue=u=d,s.pending=null}if(u!==null){d=u.next,a=a.baseState;var y=p=null,_=null,M=d;do{var U=M.lane;if((Jr&U)===U)_!==null&&(_=_.next={lane:0,action:M.action,hasEagerState:M.hasEagerState,eagerState:M.eagerState,next:null}),a=M.hasEagerState?M.eagerState:t(a,M.action);else{var $={lane:U,action:M.action,hasEagerState:M.hasEagerState,eagerState:M.eagerState,next:null};_===null?(y=_=$,p=a):_=_.next=$,et.lanes|=U,Zr|=U}M=M.next}while(M!==null&&M!==d);_===null?p=a:_.next=y,_n(a,n.memoizedState)||(Vt=!0),n.memoizedState=a,n.baseState=p,n.baseQueue=_,s.lastRenderedState=a}if(t=s.interleaved,t!==null){u=t;do d=u.lane,et.lanes|=d,Zr|=d,u=u.next;while(u!==t)}else u===null&&(s.lanes=0);return[n.memoizedState,s.dispatch]}function yl(t){var n=pn(),s=n.queue;if(s===null)throw Error(r(311));s.lastRenderedReducer=t;var a=s.dispatch,u=s.pending,d=n.memoizedState;if(u!==null){s.pending=null;var p=u=u.next;do d=t(d,p.action),p=p.next;while(p!==u);_n(d,n.memoizedState)||(Vt=!0),n.memoizedState=d,n.baseQueue===null&&(n.baseState=d),s.lastRenderedState=d}return[d,a]}function nd(){}function rd(t,n){var s=et,a=pn(),u=n(),d=!_n(a.memoizedState,u);if(d&&(a.memoizedState=u,Vt=!0),a=a.queue,wl(od.bind(null,s,a,t),[t]),a.getSnapshot!==n||d||pt!==null&&pt.memoizedState.tag&1){if(s.flags|=2048,xs(9,sd.bind(null,s,a,u,n),void 0,null),mt===null)throw Error(r(349));(Jr&30)!==0||id(s,n,u)}return u}function id(t,n,s){t.flags|=16384,t={getSnapshot:n,value:s},n=et.updateQueue,n===null?(n={lastEffect:null,stores:null},et.updateQueue=n,n.stores=[t]):(s=n.stores,s===null?n.stores=[t]:s.push(t))}function sd(t,n,s,a){n.value=s,n.getSnapshot=a,ad(n)&&ld(t)}function od(t,n,s){return s(function(){ad(n)&&ld(t)})}function ad(t){var n=t.getSnapshot;t=t.value;try{var s=n();return!_n(t,s)}catch{return!0}}function ld(t){var n=Zn(t,1);n!==null&&Cn(n,t,1,-1)}function ud(t){var n=Fn();return typeof t=="function"&&(t=t()),n.memoizedState=n.baseState=t,t={pending:null,interleaved:null,lanes:0,dispatch:null,lastRenderedReducer:ws,lastRenderedState:t},n.queue=t,t=t.dispatch=yg.bind(null,et,t),[n.memoizedState,t]}function xs(t,n,s,a){return t={tag:t,create:n,destroy:s,deps:a,next:null},n=et.updateQueue,n===null?(n={lastEffect:null,stores:null},et.updateQueue=n,n.lastEffect=t.next=t):(s=n.lastEffect,s===null?n.lastEffect=t.next=t:(a=s.next,s.next=t,t.next=a,n.lastEffect=t)),t}function cd(){return pn().memoizedState}function So(t,n,s,a){var u=Fn();et.flags|=t,u.memoizedState=xs(1|n,s,void 0,a===void 0?null:a)}function ko(t,n,s,a){var u=pn();a=a===void 0?null:a;var d=void 0;if(dt!==null){var p=dt.memoizedState;if(d=p.destroy,a!==null&&pl(a,p.deps)){u.memoizedState=xs(n,s,d,a);return}}et.flags|=t,u.memoizedState=xs(1|n,s,d,a)}function dd(t,n){return So(8390656,8,t,n)}function wl(t,n){return ko(2048,8,t,n)}function hd(t,n){return ko(4,2,t,n)}function fd(t,n){return ko(4,4,t,n)}function pd(t,n){if(typeof n=="function")return t=t(),n(t),function(){n(null)};if(n!=null)return t=t(),n.current=t,function(){n.current=null}}function md(t,n,s){return s=s!=null?s.concat([t]):null,ko(4,4,pd.bind(null,n,t),s)}function xl(){}function gd(t,n){var s=pn();n=n===void 0?null:n;var a=s.memoizedState;return a!==null&&n!==null&&pl(n,a[1])?a[0]:(s.memoizedState=[t,n],t)}function vd(t,n){var s=pn();n=n===void 0?null:n;var a=s.memoizedState;return a!==null&&n!==null&&pl(n,a[1])?a[0]:(t=t(),s.memoizedState=[t,n],t)}function yd(t,n,s){return(Jr&21)===0?(t.baseState&&(t.baseState=!1,Vt=!0),t.memoizedState=s):(_n(s,n)||(s=Ut(),et.lanes|=s,Zr|=s,t.baseState=!0),n)}function gg(t,n){var s=$e;$e=s!==0&&4>s?s:4,t(!0);var a=fl.transition;fl.transition={};try{t(!1),n()}finally{$e=s,fl.transition=a}}function wd(){return pn().memoizedState}function vg(t,n,s){var a=Pr(t);if(s={lane:a,action:s,hasEagerState:!1,eagerState:null,next:null},xd(t))_d(n,s);else if(s=Qc(t,n,s,a),s!==null){var u=Dt();Cn(s,t,a,u),Ed(s,n,a)}}function yg(t,n,s){var a=Pr(t),u={lane:a,action:s,hasEagerState:!1,eagerState:null,next:null};if(xd(t))_d(n,u);else{var d=t.alternate;if(t.lanes===0&&(d===null||d.lanes===0)&&(d=n.lastRenderedReducer,d!==null))try{var p=n.lastRenderedState,y=d(p,s);if(u.hasEagerState=!0,u.eagerState=y,_n(y,p)){var _=n.interleaved;_===null?(u.next=u,al(n)):(u.next=_.next,_.next=u),n.interleaved=u;return}}catch{}finally{}s=Qc(t,n,u,a),s!==null&&(u=Dt(),Cn(s,t,a,u),Ed(s,n,a))}}function xd(t){var n=t.alternate;return t===et||n!==null&&n===et}function _d(t,n){vs=Eo=!0;var s=t.pending;s===null?n.next=n:(n.next=s.next,s.next=n),t.pending=n}function Ed(t,n,s){if((s&4194240)!==0){var a=n.lanes;a&=t.pendingLanes,s|=a,n.lanes=s,xn(t,s)}}var To={readContext:fn,useCallback:Ct,useContext:Ct,useEffect:Ct,useImperativeHandle:Ct,useInsertionEffect:Ct,useLayoutEffect:Ct,useMemo:Ct,useReducer:Ct,useRef:Ct,useState:Ct,useDebugValue:Ct,useDeferredValue:Ct,useTransition:Ct,useMutableSource:Ct,useSyncExternalStore:Ct,useId:Ct,unstable_isNewReconciler:!1},wg={readContext:fn,useCallback:function(t,n){return Fn().memoizedState=[t,n===void 0?null:n],t},useContext:fn,useEffect:dd,useImperativeHandle:function(t,n,s){return s=s!=null?s.concat([t]):null,So(4194308,4,pd.bind(null,n,t),s)},useLayoutEffect:function(t,n){return So(4194308,4,t,n)},useInsertionEffect:function(t,n){return So(4,2,t,n)},useMemo:function(t,n){var s=Fn();return n=n===void 0?null:n,t=t(),s.memoizedState=[t,n],t},useReducer:function(t,n,s){var a=Fn();return n=s!==void 0?s(n):n,a.memoizedState=a.baseState=n,t={pending:null,interleaved:null,lanes:0,dispatch:null,lastRenderedReducer:t,lastRenderedState:n},a.queue=t,t=t.dispatch=vg.bind(null,et,t),[a.memoizedState,t]},useRef:function(t){var n=Fn();return t={current:t},n.memoizedState=t},useState:ud,useDebugValue:xl,useDeferredValue:function(t){return Fn().memoizedState=t},useTransition:function(){var t=ud(!1),n=t[0];return t=gg.bind(null,t[1]),Fn().memoizedState=t,[n,t]},useMutableSource:function(){},useSyncExternalStore:function(t,n,s){var a=et,u=Fn();if(Je){if(s===void 0)throw Error(r(407));s=s()}else{if(s=n(),mt===null)throw Error(r(349));(Jr&30)!==0||id(a,n,s)}u.memoizedState=s;var d={value:s,getSnapshot:n};return u.queue=d,dd(od.bind(null,a,d,t),[t]),a.flags|=2048,xs(9,sd.bind(null,a,d,s,n),void 0,null),s},useId:function(){var t=Fn(),n=mt.identifierPrefix;if(Je){var s=Jn,a=Qn;s=(a&~(1<<32-jt(a)-1)).toString(32)+s,n=":"+n+"R"+s,s=ys++,0<s&&(n+="H"+s.toString(32)),n+=":"}else s=mg++,n=":"+n+"r"+s.toString(32)+":";return t.memoizedState=n},unstable_isNewReconciler:!1},xg={readContext:fn,useCallback:gd,useContext:fn,useEffect:wl,useImperativeHandle:md,useInsertionEffect:hd,useLayoutEffect:fd,useMemo:vd,useReducer:vl,useRef:cd,useState:function(){return vl(ws)},useDebugValue:xl,useDeferredValue:function(t){var n=pn();return yd(n,dt.memoizedState,t)},useTransition:function(){var t=vl(ws)[0],n=pn().memoizedState;return[t,n]},useMutableSource:nd,useSyncExternalStore:rd,useId:wd,unstable_isNewReconciler:!1},_g={readContext:fn,useCallback:gd,useContext:fn,useEffect:wl,useImperativeHandle:md,useInsertionEffect:hd,useLayoutEffect:fd,useMemo:vd,useReducer:yl,useRef:cd,useState:function(){return yl(ws)},useDebugValue:xl,useDeferredValue:function(t){var n=pn();return dt===null?n.memoizedState=t:yd(n,dt.memoizedState,t)},useTransition:function(){var t=yl(ws)[0],n=pn().memoizedState;return[t,n]},useMutableSource:nd,useSyncExternalStore:rd,useId:wd,unstable_isNewReconciler:!1};function Sn(t,n){if(t&&t.defaultProps){n=Y({},n),t=t.defaultProps;for(var s in t)n[s]===void 0&&(n[s]=t[s]);return n}return n}function _l(t,n,s,a){n=t.memoizedState,s=s(a,n),s=s==null?n:Y({},n,s),t.memoizedState=s,t.lanes===0&&(t.updateQueue.baseState=s)}var Co={isMounted:function(t){return(t=t._reactInternals)?bn(t)===t:!1},enqueueSetState:function(t,n,s){t=t._reactInternals;var a=Dt(),u=Pr(t),d=er(a,u);d.payload=n,s!=null&&(d.callback=s),n=Cr(t,d,u),n!==null&&(Cn(n,t,u,a),yo(n,t,u))},enqueueReplaceState:function(t,n,s){t=t._reactInternals;var a=Dt(),u=Pr(t),d=er(a,u);d.tag=1,d.payload=n,s!=null&&(d.callback=s),n=Cr(t,d,u),n!==null&&(Cn(n,t,u,a),yo(n,t,u))},enqueueForceUpdate:function(t,n){t=t._reactInternals;var s=Dt(),a=Pr(t),u=er(s,a);u.tag=2,n!=null&&(u.callback=n),n=Cr(t,u,a),n!==null&&(Cn(n,t,a,s),yo(n,t,a))}};function Sd(t,n,s,a,u,d,p){return t=t.stateNode,typeof t.shouldComponentUpdate=="function"?t.shouldComponentUpdate(a,d,p):n.prototype&&n.prototype.isPureReactComponent?!os(s,a)||!os(u,d):!0}function kd(t,n,s){var a=!1,u=Sr,d=n.contextType;return typeof d=="object"&&d!==null?d=fn(d):(u=$t(n)?qr:Tt.current,a=n.contextTypes,d=(a=a!=null)?ki(t,u):Sr),n=new n(s,d),t.memoizedState=n.state!==null&&n.state!==void 0?n.state:null,n.updater=Co,t.stateNode=n,n._reactInternals=t,a&&(t=t.stateNode,t.__reactInternalMemoizedUnmaskedChildContext=u,t.__reactInternalMemoizedMaskedChildContext=d),n}function Td(t,n,s,a){t=n.state,typeof n.componentWillReceiveProps=="function"&&n.componentWillReceiveProps(s,a),typeof n.UNSAFE_componentWillReceiveProps=="function"&&n.UNSAFE_componentWillReceiveProps(s,a),n.state!==t&&Co.enqueueReplaceState(n,n.state,null)}function El(t,n,s,a){var u=t.stateNode;u.props=s,u.state=t.memoizedState,u.refs={},ll(t);var d=n.contextType;typeof d=="object"&&d!==null?u.context=fn(d):(d=$t(n)?qr:Tt.current,u.context=ki(t,d)),u.state=t.memoizedState,d=n.getDerivedStateFromProps,typeof d=="function"&&(_l(t,n,d,s),u.state=t.memoizedState),typeof n.getDerivedStateFromProps=="function"||typeof u.getSnapshotBeforeUpdate=="function"||typeof u.UNSAFE_componentWillMount!="function"&&typeof u.componentWillMount!="function"||(n=u.state,typeof u.componentWillMount=="function"&&u.componentWillMount(),typeof u.UNSAFE_componentWillMount=="function"&&u.UNSAFE_componentWillMount(),n!==u.state&&Co.enqueueReplaceState(u,u.state,null),wo(t,s,u,a),u.state=t.memoizedState),typeof u.componentDidMount=="function"&&(t.flags|=4194308)}function Mi(t,n){try{var s="",a=n;do s+=ke(a),a=a.return;while(a);var u=s}catch(d){u=`
Error generating stack: `+d.message+`
`+d.stack}return{value:t,source:n,stack:u,digest:null}}function Sl(t,n,s){return{value:t,source:null,stack:s??null,digest:n??null}}function kl(t,n){try{console.error(n.value)}catch(s){setTimeout(function(){throw s})}}var Eg=typeof WeakMap=="function"?WeakMap:Map;function Cd(t,n,s){s=er(-1,s),s.tag=3,s.payload={element:null};var a=n.value;return s.callback=function(){Do||(Do=!0,jl=a),kl(t,n)},s}function Id(t,n,s){s=er(-1,s),s.tag=3;var a=t.type.getDerivedStateFromError;if(typeof a=="function"){var u=n.value;s.payload=function(){return a(u)},s.callback=function(){kl(t,n)}}var d=t.stateNode;return d!==null&&typeof d.componentDidCatch=="function"&&(s.callback=function(){kl(t,n),typeof a!="function"&&(Rr===null?Rr=new Set([this]):Rr.add(this));var p=n.stack;this.componentDidCatch(n.value,{componentStack:p!==null?p:""})}),s}function Rd(t,n,s){var a=t.pingCache;if(a===null){a=t.pingCache=new Eg;var u=new Set;a.set(n,u)}else u=a.get(n),u===void 0&&(u=new Set,a.set(n,u));u.has(s)||(u.add(s),t=Og.bind(null,t,n,s),n.then(t,t))}function Nd(t){do{var n;if((n=t.tag===13)&&(n=t.memoizedState,n=n!==null?n.dehydrated!==null:!0),n)return t;t=t.return}while(t!==null);return null}function Pd(t,n,s,a,u){return(t.mode&1)===0?(t===n?t.flags|=65536:(t.flags|=128,s.flags|=131072,s.flags&=-52805,s.tag===1&&(s.alternate===null?s.tag=17:(n=er(-1,1),n.tag=2,Cr(s,n,1))),s.lanes|=1),t):(t.flags|=65536,t.lanes=u,t)}var Sg=B.ReactCurrentOwner,Vt=!1;function Mt(t,n,s,a){n.child=t===null?Yc(n,null,s,a):Ri(n,t.child,s,a)}function Ad(t,n,s,a,u){s=s.render;var d=n.ref;return Pi(n,u),a=ml(t,n,s,a,d,u),s=gl(),t!==null&&!Vt?(n.updateQueue=t.updateQueue,n.flags&=-2053,t.lanes&=~u,tr(t,n,u)):(Je&&s&&Ja(n),n.flags|=1,Mt(t,n,a,u),n.child)}function Md(t,n,s,a,u){if(t===null){var d=s.type;return typeof d=="function"&&!Gl(d)&&d.defaultProps===void 0&&s.compare===null&&s.defaultProps===void 0?(n.tag=15,n.type=d,Dd(t,n,d,a,u)):(t=jo(s.type,null,a,n,n.mode,u),t.ref=n.ref,t.return=n,n.child=t)}if(d=t.child,(t.lanes&u)===0){var p=d.memoizedProps;if(s=s.compare,s=s!==null?s:os,s(p,a)&&t.ref===n.ref)return tr(t,n,u)}return n.flags|=1,t=Mr(d,a),t.ref=n.ref,t.return=n,n.child=t}function Dd(t,n,s,a,u){if(t!==null){var d=t.memoizedProps;if(os(d,a)&&t.ref===n.ref)if(Vt=!1,n.pendingProps=a=d,(t.lanes&u)!==0)(t.flags&131072)!==0&&(Vt=!0);else return n.lanes=t.lanes,tr(t,n,u)}return Tl(t,n,s,a,u)}function bd(t,n,s){var a=n.pendingProps,u=a.children,d=t!==null?t.memoizedState:null;if(a.mode==="hidden")if((n.mode&1)===0)n.memoizedState={baseLanes:0,cachePool:null,transitions:null},qe(bi,nn),nn|=s;else{if((s&1073741824)===0)return t=d!==null?d.baseLanes|s:s,n.lanes=n.childLanes=1073741824,n.memoizedState={baseLanes:t,cachePool:null,transitions:null},n.updateQueue=null,qe(bi,nn),nn|=t,null;n.memoizedState={baseLanes:0,cachePool:null,transitions:null},a=d!==null?d.baseLanes:s,qe(bi,nn),nn|=a}else d!==null?(a=d.baseLanes|s,n.memoizedState=null):a=s,qe(bi,nn),nn|=a;return Mt(t,n,u,s),n.child}function Ld(t,n){var s=n.ref;(t===null&&s!==null||t!==null&&t.ref!==s)&&(n.flags|=512,n.flags|=2097152)}function Tl(t,n,s,a,u){var d=$t(s)?qr:Tt.current;return d=ki(n,d),Pi(n,u),s=ml(t,n,s,a,d,u),a=gl(),t!==null&&!Vt?(n.updateQueue=t.updateQueue,n.flags&=-2053,t.lanes&=~u,tr(t,n,u)):(Je&&a&&Ja(n),n.flags|=1,Mt(t,n,s,u),n.child)}function Od(t,n,s,a,u){if($t(s)){var d=!0;uo(n)}else d=!1;if(Pi(n,u),n.stateNode===null)Ro(t,n),kd(n,s,a),El(n,s,a,u),a=!0;else if(t===null){var p=n.stateNode,y=n.memoizedProps;p.props=y;var _=p.context,M=s.contextType;typeof M=="object"&&M!==null?M=fn(M):(M=$t(s)?qr:Tt.current,M=ki(n,M));var U=s.getDerivedStateFromProps,$=typeof U=="function"||typeof p.getSnapshotBeforeUpdate=="function";$||typeof p.UNSAFE_componentWillReceiveProps!="function"&&typeof p.componentWillReceiveProps!="function"||(y!==a||_!==M)&&Td(n,p,a,M),Tr=!1;var z=n.memoizedState;p.state=z,wo(n,a,p,u),_=n.memoizedState,y!==a||z!==_||Bt.current||Tr?(typeof U=="function"&&(_l(n,s,U,a),_=n.memoizedState),(y=Tr||Sd(n,s,y,a,z,_,M))?($||typeof p.UNSAFE_componentWillMount!="function"&&typeof p.componentWillMount!="function"||(typeof p.componentWillMount=="function"&&p.componentWillMount(),typeof p.UNSAFE_componentWillMount=="function"&&p.UNSAFE_componentWillMount()),typeof p.componentDidMount=="function"&&(n.flags|=4194308)):(typeof p.componentDidMount=="function"&&(n.flags|=4194308),n.memoizedProps=a,n.memoizedState=_),p.props=a,p.state=_,p.context=M,a=y):(typeof p.componentDidMount=="function"&&(n.flags|=4194308),a=!1)}else{p=n.stateNode,Jc(t,n),y=n.memoizedProps,M=n.type===n.elementType?y:Sn(n.type,y),p.props=M,$=n.pendingProps,z=p.context,_=s.contextType,typeof _=="object"&&_!==null?_=fn(_):(_=$t(s)?qr:Tt.current,_=ki(n,_));var Z=s.getDerivedStateFromProps;(U=typeof Z=="function"||typeof p.getSnapshotBeforeUpdate=="function")||typeof p.UNSAFE_componentWillReceiveProps!="function"&&typeof p.componentWillReceiveProps!="function"||(y!==$||z!==_)&&Td(n,p,a,_),Tr=!1,z=n.memoizedState,p.state=z,wo(n,a,p,u);var ie=n.memoizedState;y!==$||z!==ie||Bt.current||Tr?(typeof Z=="function"&&(_l(n,s,Z,a),ie=n.memoizedState),(M=Tr||Sd(n,s,M,a,z,ie,_)||!1)?(U||typeof p.UNSAFE_componentWillUpdate!="function"&&typeof p.componentWillUpdate!="function"||(typeof p.componentWillUpdate=="function"&&p.componentWillUpdate(a,ie,_),typeof p.UNSAFE_componentWillUpdate=="function"&&p.UNSAFE_componentWillUpdate(a,ie,_)),typeof p.componentDidUpdate=="function"&&(n.flags|=4),typeof p.getSnapshotBeforeUpdate=="function"&&(n.flags|=1024)):(typeof p.componentDidUpdate!="function"||y===t.memoizedProps&&z===t.memoizedState||(n.flags|=4),typeof p.getSnapshotBeforeUpdate!="function"||y===t.memoizedProps&&z===t.memoizedState||(n.flags|=1024),n.memoizedProps=a,n.memoizedState=ie),p.props=a,p.state=ie,p.context=_,a=M):(typeof p.componentDidUpdate!="function"||y===t.memoizedProps&&z===t.memoizedState||(n.flags|=4),typeof p.getSnapshotBeforeUpdate!="function"||y===t.memoizedProps&&z===t.memoizedState||(n.flags|=1024),a=!1)}return Cl(t,n,s,a,d,u)}function Cl(t,n,s,a,u,d){Ld(t,n);var p=(n.flags&128)!==0;if(!a&&!p)return u&&Bc(n,s,!1),tr(t,n,d);a=n.stateNode,Sg.current=n;var y=p&&typeof s.getDerivedStateFromError!="function"?null:a.render();return n.flags|=1,t!==null&&p?(n.child=Ri(n,t.child,null,d),n.child=Ri(n,null,y,d)):Mt(t,n,y,d),n.memoizedState=a.state,u&&Bc(n,s,!0),n.child}function Fd(t){var n=t.stateNode;n.pendingContext?jc(t,n.pendingContext,n.pendingContext!==n.context):n.context&&jc(t,n.context,!1),ul(t,n.containerInfo)}function zd(t,n,s,a,u){return Ii(),nl(u),n.flags|=256,Mt(t,n,s,a),n.child}var Il={dehydrated:null,treeContext:null,retryLane:0};function Rl(t){return{baseLanes:t,cachePool:null,transitions:null}}function jd(t,n,s){var a=n.pendingProps,u=Ze.current,d=!1,p=(n.flags&128)!==0,y;if((y=p)||(y=t!==null&&t.memoizedState===null?!1:(u&2)!==0),y?(d=!0,n.flags&=-129):(t===null||t.memoizedState!==null)&&(u|=1),qe(Ze,u&1),t===null)return tl(n),t=n.memoizedState,t!==null&&(t=t.dehydrated,t!==null)?((n.mode&1)===0?n.lanes=1:t.data==="$!"?n.lanes=8:n.lanes=1073741824,null):(p=a.children,t=a.fallback,d?(a=n.mode,d=n.child,p={mode:"hidden",children:p},(a&1)===0&&d!==null?(d.childLanes=0,d.pendingProps=p):d=Uo(p,a,0,null),t=ri(t,a,s,null),d.return=n,t.return=n,d.sibling=t,n.child=d,n.child.memoizedState=Rl(s),n.memoizedState=Il,t):Nl(n,p));if(u=t.memoizedState,u!==null&&(y=u.dehydrated,y!==null))return kg(t,n,p,a,y,u,s);if(d){d=a.fallback,p=n.mode,u=t.child,y=u.sibling;var _={mode:"hidden",children:a.children};return(p&1)===0&&n.child!==u?(a=n.child,a.childLanes=0,a.pendingProps=_,n.deletions=null):(a=Mr(u,_),a.subtreeFlags=u.subtreeFlags&14680064),y!==null?d=Mr(y,d):(d=ri(d,p,s,null),d.flags|=2),d.return=n,a.return=n,a.sibling=d,n.child=a,a=d,d=n.child,p=t.child.memoizedState,p=p===null?Rl(s):{baseLanes:p.baseLanes|s,cachePool:null,transitions:p.transitions},d.memoizedState=p,d.childLanes=t.childLanes&~s,n.memoizedState=Il,a}return d=t.child,t=d.sibling,a=Mr(d,{mode:"visible",children:a.children}),(n.mode&1)===0&&(a.lanes=s),a.return=n,a.sibling=null,t!==null&&(s=n.deletions,s===null?(n.deletions=[t],n.flags|=16):s.push(t)),n.child=a,n.memoizedState=null,a}function Nl(t,n){return n=Uo({mode:"visible",children:n},t.mode,0,null),n.return=t,t.child=n}function Io(t,n,s,a){return a!==null&&nl(a),Ri(n,t.child,null,s),t=Nl(n,n.pendingProps.children),t.flags|=2,n.memoizedState=null,t}function kg(t,n,s,a,u,d,p){if(s)return n.flags&256?(n.flags&=-257,a=Sl(Error(r(422))),Io(t,n,p,a)):n.memoizedState!==null?(n.child=t.child,n.flags|=128,null):(d=a.fallback,u=n.mode,a=Uo({mode:"visible",children:a.children},u,0,null),d=ri(d,u,p,null),d.flags|=2,a.return=n,d.return=n,a.sibling=d,n.child=a,(n.mode&1)!==0&&Ri(n,t.child,null,p),n.child.memoizedState=Rl(p),n.memoizedState=Il,d);if((n.mode&1)===0)return Io(t,n,p,null);if(u.data==="$!"){if(a=u.nextSibling&&u.nextSibling.dataset,a)var y=a.dgst;return a=y,d=Error(r(419)),a=Sl(d,a,void 0),Io(t,n,p,a)}if(y=(p&t.childLanes)!==0,Vt||y){if(a=mt,a!==null){switch(p&-p){case 4:u=2;break;case 16:u=8;break;case 64:case 128:case 256:case 512:case 1024:case 2048:case 4096:case 8192:case 16384:case 32768:case 65536:case 131072:case 262144:case 524288:case 1048576:case 2097152:case 4194304:case 8388608:case 16777216:case 33554432:case 67108864:u=32;break;case 536870912:u=268435456;break;default:u=0}u=(u&(a.suspendedLanes|p))!==0?0:u,u!==0&&u!==d.retryLane&&(d.retryLane=u,Zn(t,u),Cn(a,t,u,-1))}return Wl(),a=Sl(Error(r(421))),Io(t,n,p,a)}return u.data==="$?"?(n.flags|=128,n.child=t.child,n=Fg.bind(null,t),u._reactRetry=n,null):(t=d.treeContext,tn=_r(u.nextSibling),en=n,Je=!0,En=null,t!==null&&(dn[hn++]=Qn,dn[hn++]=Jn,dn[hn++]=Kr,Qn=t.id,Jn=t.overflow,Kr=n),n=Nl(n,a.children),n.flags|=4096,n)}function Ud(t,n,s){t.lanes|=n;var a=t.alternate;a!==null&&(a.lanes|=n),ol(t.return,n,s)}function Pl(t,n,s,a,u){var d=t.memoizedState;d===null?t.memoizedState={isBackwards:n,rendering:null,renderingStartTime:0,last:a,tail:s,tailMode:u}:(d.isBackwards=n,d.rendering=null,d.renderingStartTime=0,d.last=a,d.tail=s,d.tailMode=u)}function Bd(t,n,s){var a=n.pendingProps,u=a.revealOrder,d=a.tail;if(Mt(t,n,a.children,s),a=Ze.current,(a&2)!==0)a=a&1|2,n.flags|=128;else{if(t!==null&&(t.flags&128)!==0)e:for(t=n.child;t!==null;){if(t.tag===13)t.memoizedState!==null&&Ud(t,s,n);else if(t.tag===19)Ud(t,s,n);else if(t.child!==null){t.child.return=t,t=t.child;continue}if(t===n)break e;for(;t.sibling===null;){if(t.return===null||t.return===n)break e;t=t.return}t.sibling.return=t.return,t=t.sibling}a&=1}if(qe(Ze,a),(n.mode&1)===0)n.memoizedState=null;else switch(u){case"forwards":for(s=n.child,u=null;s!==null;)t=s.alternate,t!==null&&xo(t)===null&&(u=s),s=s.sibling;s=u,s===null?(u=n.child,n.child=null):(u=s.sibling,s.sibling=null),Pl(n,!1,u,s,d);break;case"backwards":for(s=null,u=n.child,n.child=null;u!==null;){if(t=u.alternate,t!==null&&xo(t)===null){n.child=u;break}t=u.sibling,u.sibling=s,s=u,u=t}Pl(n,!0,s,null,d);break;case"together":Pl(n,!1,null,null,void 0);break;default:n.memoizedState=null}return n.child}function Ro(t,n){(n.mode&1)===0&&t!==null&&(t.alternate=null,n.alternate=null,n.flags|=2)}function tr(t,n,s){if(t!==null&&(n.dependencies=t.dependencies),Zr|=n.lanes,(s&n.childLanes)===0)return null;if(t!==null&&n.child!==t.child)throw Error(r(153));if(n.child!==null){for(t=n.child,s=Mr(t,t.pendingProps),n.child=s,s.return=n;t.sibling!==null;)t=t.sibling,s=s.sibling=Mr(t,t.pendingProps),s.return=n;s.sibling=null}return n.child}function Tg(t,n,s){switch(n.tag){case 3:Fd(n),Ii();break;case 5:td(n);break;case 1:$t(n.type)&&uo(n);break;case 4:ul(n,n.stateNode.containerInfo);break;case 10:var a=n.type._context,u=n.memoizedProps.value;qe(go,a._currentValue),a._currentValue=u;break;case 13:if(a=n.memoizedState,a!==null)return a.dehydrated!==null?(qe(Ze,Ze.current&1),n.flags|=128,null):(s&n.child.childLanes)!==0?jd(t,n,s):(qe(Ze,Ze.current&1),t=tr(t,n,s),t!==null?t.sibling:null);qe(Ze,Ze.current&1);break;case 19:if(a=(s&n.childLanes)!==0,(t.flags&128)!==0){if(a)return Bd(t,n,s);n.flags|=128}if(u=n.memoizedState,u!==null&&(u.rendering=null,u.tail=null,u.lastEffect=null),qe(Ze,Ze.current),a)break;return null;case 22:case 23:return n.lanes=0,bd(t,n,s)}return tr(t,n,s)}var $d,Al,Vd,Hd;$d=function(t,n){for(var s=n.child;s!==null;){if(s.tag===5||s.tag===6)t.appendChild(s.stateNode);else if(s.tag!==4&&s.child!==null){s.child.return=s,s=s.child;continue}if(s===n)break;for(;s.sibling===null;){if(s.return===null||s.return===n)return;s=s.return}s.sibling.return=s.return,s=s.sibling}},Al=function(){},Vd=function(t,n,s,a){var u=t.memoizedProps;if(u!==a){t=n.stateNode,Qr(On.current);var d=null;switch(s){case"input":u=Be(t,u),a=Be(t,a),d=[];break;case"select":u=Y({},u,{value:void 0}),a=Y({},a,{value:void 0}),d=[];break;case"textarea":u=Ot(t,u),a=Ot(t,a),d=[];break;default:typeof u.onClick!="function"&&typeof a.onClick=="function"&&(t.onclick=oo)}V(s,a);var p;s=null;for(M in u)if(!a.hasOwnProperty(M)&&u.hasOwnProperty(M)&&u[M]!=null)if(M==="style"){var y=u[M];for(p in y)y.hasOwnProperty(p)&&(s||(s={}),s[p]="")}else M!=="dangerouslySetInnerHTML"&&M!=="children"&&M!=="suppressContentEditableWarning"&&M!=="suppressHydrationWarning"&&M!=="autoFocus"&&(l.hasOwnProperty(M)?d||(d=[]):(d=d||[]).push(M,null));for(M in a){var _=a[M];if(y=u!=null?u[M]:void 0,a.hasOwnProperty(M)&&_!==y&&(_!=null||y!=null))if(M==="style")if(y){for(p in y)!y.hasOwnProperty(p)||_&&_.hasOwnProperty(p)||(s||(s={}),s[p]="");for(p in _)_.hasOwnProperty(p)&&y[p]!==_[p]&&(s||(s={}),s[p]=_[p])}else s||(d||(d=[]),d.push(M,s)),s=_;else M==="dangerouslySetInnerHTML"?(_=_?_.__html:void 0,y=y?y.__html:void 0,_!=null&&y!==_&&(d=d||[]).push(M,_)):M==="children"?typeof _!="string"&&typeof _!="number"||(d=d||[]).push(M,""+_):M!=="suppressContentEditableWarning"&&M!=="suppressHydrationWarning"&&(l.hasOwnProperty(M)?(_!=null&&M==="onScroll"&&Ke("scroll",t),d||y===_||(d=[])):(d=d||[]).push(M,_))}s&&(d=d||[]).push("style",s);var M=d;(n.updateQueue=M)&&(n.flags|=4)}},Hd=function(t,n,s,a){s!==a&&(n.flags|=4)};function _s(t,n){if(!Je)switch(t.tailMode){case"hidden":n=t.tail;for(var s=null;n!==null;)n.alternate!==null&&(s=n),n=n.sibling;s===null?t.tail=null:s.sibling=null;break;case"collapsed":s=t.tail;for(var a=null;s!==null;)s.alternate!==null&&(a=s),s=s.sibling;a===null?n||t.tail===null?t.tail=null:t.tail.sibling=null:a.sibling=null}}function It(t){var n=t.alternate!==null&&t.alternate.child===t.child,s=0,a=0;if(n)for(var u=t.child;u!==null;)s|=u.lanes|u.childLanes,a|=u.subtreeFlags&14680064,a|=u.flags&14680064,u.return=t,u=u.sibling;else for(u=t.child;u!==null;)s|=u.lanes|u.childLanes,a|=u.subtreeFlags,a|=u.flags,u.return=t,u=u.sibling;return t.subtreeFlags|=a,t.childLanes=s,n}function Cg(t,n,s){var a=n.pendingProps;switch(Za(n),n.tag){case 2:case 16:case 15:case 0:case 11:case 7:case 8:case 12:case 9:case 14:return It(n),null;case 1:return $t(n.type)&&lo(),It(n),null;case 3:return a=n.stateNode,Ai(),Xe(Bt),Xe(Tt),hl(),a.pendingContext&&(a.context=a.pendingContext,a.pendingContext=null),(t===null||t.child===null)&&(po(n)?n.flags|=4:t===null||t.memoizedState.isDehydrated&&(n.flags&256)===0||(n.flags|=1024,En!==null&&($l(En),En=null))),Al(t,n),It(n),null;case 5:cl(n);var u=Qr(gs.current);if(s=n.type,t!==null&&n.stateNode!=null)Vd(t,n,s,a,u),t.ref!==n.ref&&(n.flags|=512,n.flags|=2097152);else{if(!a){if(n.stateNode===null)throw Error(r(166));return It(n),null}if(t=Qr(On.current),po(n)){a=n.stateNode,s=n.type;var d=n.memoizedProps;switch(a[Ln]=n,a[ds]=d,t=(n.mode&1)!==0,s){case"dialog":Ke("cancel",a),Ke("close",a);break;case"iframe":case"object":case"embed":Ke("load",a);break;case"video":case"audio":for(u=0;u<ls.length;u++)Ke(ls[u],a);break;case"source":Ke("error",a);break;case"img":case"image":case"link":Ke("error",a),Ke("load",a);break;case"details":Ke("toggle",a);break;case"input":sn(a,d),Ke("invalid",a);break;case"select":a._wrapperState={wasMultiple:!!d.multiple},Ke("invalid",a);break;case"textarea":an(a,d),Ke("invalid",a)}V(s,d),u=null;for(var p in d)if(d.hasOwnProperty(p)){var y=d[p];p==="children"?typeof y=="string"?a.textContent!==y&&(d.suppressHydrationWarning!==!0&&so(a.textContent,y,t),u=["children",y]):typeof y=="number"&&a.textContent!==""+y&&(d.suppressHydrationWarning!==!0&&so(a.textContent,y,t),u=["children",""+y]):l.hasOwnProperty(p)&&y!=null&&p==="onScroll"&&Ke("scroll",a)}switch(s){case"input":He(a),Mn(a,d,!0);break;case"textarea":He(a),ot(a);break;case"select":case"option":break;default:typeof d.onClick=="function"&&(a.onclick=oo)}a=u,n.updateQueue=a,a!==null&&(n.flags|=4)}else{p=u.nodeType===9?u:u.ownerDocument,t==="http://www.w3.org/1999/xhtml"&&(t=it(s)),t==="http://www.w3.org/1999/xhtml"?s==="script"?(t=p.createElement("div"),t.innerHTML="<script><\/script>",t=t.removeChild(t.firstChild)):typeof a.is=="string"?t=p.createElement(s,{is:a.is}):(t=p.createElement(s),s==="select"&&(p=t,a.multiple?p.multiple=!0:a.size&&(p.size=a.size))):t=p.createElementNS(t,s),t[Ln]=n,t[ds]=a,$d(t,n,!1,!1),n.stateNode=t;e:{switch(p=J(s,a),s){case"dialog":Ke("cancel",t),Ke("close",t),u=a;break;case"iframe":case"object":case"embed":Ke("load",t),u=a;break;case"video":case"audio":for(u=0;u<ls.length;u++)Ke(ls[u],t);u=a;break;case"source":Ke("error",t),u=a;break;case"img":case"image":case"link":Ke("error",t),Ke("load",t),u=a;break;case"details":Ke("toggle",t),u=a;break;case"input":sn(t,a),u=Be(t,a),Ke("invalid",t);break;case"option":u=a;break;case"select":t._wrapperState={wasMultiple:!!a.multiple},u=Y({},a,{value:void 0}),Ke("invalid",t);break;case"textarea":an(t,a),u=Ot(t,a),Ke("invalid",t);break;default:u=a}V(s,u),y=u;for(d in y)if(y.hasOwnProperty(d)){var _=y[d];d==="style"?G(t,_):d==="dangerouslySetInnerHTML"?(_=_?_.__html:void 0,_!=null&&Kt(t,_)):d==="children"?typeof _=="string"?(s!=="textarea"||_!=="")&&Ft(t,_):typeof _=="number"&&Ft(t,""+_):d!=="suppressContentEditableWarning"&&d!=="suppressHydrationWarning"&&d!=="autoFocus"&&(l.hasOwnProperty(d)?_!=null&&d==="onScroll"&&Ke("scroll",t):_!=null&&q(t,d,_,p))}switch(s){case"input":He(t),Mn(t,a,!1);break;case"textarea":He(t),ot(t);break;case"option":a.value!=null&&t.setAttribute("value",""+te(a.value));break;case"select":t.multiple=!!a.multiple,d=a.value,d!=null?Fe(t,!!a.multiple,d,!1):a.defaultValue!=null&&Fe(t,!!a.multiple,a.defaultValue,!0);break;default:typeof u.onClick=="function"&&(t.onclick=oo)}switch(s){case"button":case"input":case"select":case"textarea":a=!!a.autoFocus;break e;case"img":a=!0;break e;default:a=!1}}a&&(n.flags|=4)}n.ref!==null&&(n.flags|=512,n.flags|=2097152)}return It(n),null;case 6:if(t&&n.stateNode!=null)Hd(t,n,t.memoizedProps,a);else{if(typeof a!="string"&&n.stateNode===null)throw Error(r(166));if(s=Qr(gs.current),Qr(On.current),po(n)){if(a=n.stateNode,s=n.memoizedProps,a[Ln]=n,(d=a.nodeValue!==s)&&(t=en,t!==null))switch(t.tag){case 3:so(a.nodeValue,s,(t.mode&1)!==0);break;case 5:t.memoizedProps.suppressHydrationWarning!==!0&&so(a.nodeValue,s,(t.mode&1)!==0)}d&&(n.flags|=4)}else a=(s.nodeType===9?s:s.ownerDocument).createTextNode(a),a[Ln]=n,n.stateNode=a}return It(n),null;case 13:if(Xe(Ze),a=n.memoizedState,t===null||t.memoizedState!==null&&t.memoizedState.dehydrated!==null){if(Je&&tn!==null&&(n.mode&1)!==0&&(n.flags&128)===0)qc(),Ii(),n.flags|=98560,d=!1;else if(d=po(n),a!==null&&a.dehydrated!==null){if(t===null){if(!d)throw Error(r(318));if(d=n.memoizedState,d=d!==null?d.dehydrated:null,!d)throw Error(r(317));d[Ln]=n}else Ii(),(n.flags&128)===0&&(n.memoizedState=null),n.flags|=4;It(n),d=!1}else En!==null&&($l(En),En=null),d=!0;if(!d)return n.flags&65536?n:null}return(n.flags&128)!==0?(n.lanes=s,n):(a=a!==null,a!==(t!==null&&t.memoizedState!==null)&&a&&(n.child.flags|=8192,(n.mode&1)!==0&&(t===null||(Ze.current&1)!==0?ht===0&&(ht=3):Wl())),n.updateQueue!==null&&(n.flags|=4),It(n),null);case 4:return Ai(),Al(t,n),t===null&&us(n.stateNode.containerInfo),It(n),null;case 10:return sl(n.type._context),It(n),null;case 17:return $t(n.type)&&lo(),It(n),null;case 19:if(Xe(Ze),d=n.memoizedState,d===null)return It(n),null;if(a=(n.flags&128)!==0,p=d.rendering,p===null)if(a)_s(d,!1);else{if(ht!==0||t!==null&&(t.flags&128)!==0)for(t=n.child;t!==null;){if(p=xo(t),p!==null){for(n.flags|=128,_s(d,!1),a=p.updateQueue,a!==null&&(n.updateQueue=a,n.flags|=4),n.subtreeFlags=0,a=s,s=n.child;s!==null;)d=s,t=a,d.flags&=14680066,p=d.alternate,p===null?(d.childLanes=0,d.lanes=t,d.child=null,d.subtreeFlags=0,d.memoizedProps=null,d.memoizedState=null,d.updateQueue=null,d.dependencies=null,d.stateNode=null):(d.childLanes=p.childLanes,d.lanes=p.lanes,d.child=p.child,d.subtreeFlags=0,d.deletions=null,d.memoizedProps=p.memoizedProps,d.memoizedState=p.memoizedState,d.updateQueue=p.updateQueue,d.type=p.type,t=p.dependencies,d.dependencies=t===null?null:{lanes:t.lanes,firstContext:t.firstContext}),s=s.sibling;return qe(Ze,Ze.current&1|2),n.child}t=t.sibling}d.tail!==null&&Ge()>Li&&(n.flags|=128,a=!0,_s(d,!1),n.lanes=4194304)}else{if(!a)if(t=xo(p),t!==null){if(n.flags|=128,a=!0,s=t.updateQueue,s!==null&&(n.updateQueue=s,n.flags|=4),_s(d,!0),d.tail===null&&d.tailMode==="hidden"&&!p.alternate&&!Je)return It(n),null}else 2*Ge()-d.renderingStartTime>Li&&s!==1073741824&&(n.flags|=128,a=!0,_s(d,!1),n.lanes=4194304);d.isBackwards?(p.sibling=n.child,n.child=p):(s=d.last,s!==null?s.sibling=p:n.child=p,d.last=p)}return d.tail!==null?(n=d.tail,d.rendering=n,d.tail=n.sibling,d.renderingStartTime=Ge(),n.sibling=null,s=Ze.current,qe(Ze,a?s&1|2:s&1),n):(It(n),null);case 22:case 23:return Hl(),a=n.memoizedState!==null,t!==null&&t.memoizedState!==null!==a&&(n.flags|=8192),a&&(n.mode&1)!==0?(nn&1073741824)!==0&&(It(n),n.subtreeFlags&6&&(n.flags|=8192)):It(n),null;case 24:return null;case 25:return null}throw Error(r(156,n.tag))}function Ig(t,n){switch(Za(n),n.tag){case 1:return $t(n.type)&&lo(),t=n.flags,t&65536?(n.flags=t&-65537|128,n):null;case 3:return Ai(),Xe(Bt),Xe(Tt),hl(),t=n.flags,(t&65536)!==0&&(t&128)===0?(n.flags=t&-65537|128,n):null;case 5:return cl(n),null;case 13:if(Xe(Ze),t=n.memoizedState,t!==null&&t.dehydrated!==null){if(n.alternate===null)throw Error(r(340));Ii()}return t=n.flags,t&65536?(n.flags=t&-65537|128,n):null;case 19:return Xe(Ze),null;case 4:return Ai(),null;case 10:return sl(n.type._context),null;case 22:case 23:return Hl(),null;case 24:return null;default:return null}}var No=!1,Rt=!1,Rg=typeof WeakSet=="function"?WeakSet:Set,re=null;function Di(t,n){var s=t.ref;if(s!==null)if(typeof s=="function")try{s(null)}catch(a){rt(t,n,a)}else s.current=null}function Ml(t,n,s){try{s()}catch(a){rt(t,n,a)}}var Wd=!1;function Ng(t,n){if(Ha=Ks,t=Sc(),Oa(t)){if("selectionStart"in t)var s={start:t.selectionStart,end:t.selectionEnd};else e:{s=(s=t.ownerDocument)&&s.defaultView||window;var a=s.getSelection&&s.getSelection();if(a&&a.rangeCount!==0){s=a.anchorNode;var u=a.anchorOffset,d=a.focusNode;a=a.focusOffset;try{s.nodeType,d.nodeType}catch{s=null;break e}var p=0,y=-1,_=-1,M=0,U=0,$=t,z=null;t:for(;;){for(var Z;$!==s||u!==0&&$.nodeType!==3||(y=p+u),$!==d||a!==0&&$.nodeType!==3||(_=p+a),$.nodeType===3&&(p+=$.nodeValue.length),(Z=$.firstChild)!==null;)z=$,$=Z;for(;;){if($===t)break t;if(z===s&&++M===u&&(y=p),z===d&&++U===a&&(_=p),(Z=$.nextSibling)!==null)break;$=z,z=$.parentNode}$=Z}s=y===-1||_===-1?null:{start:y,end:_}}else s=null}s=s||{start:0,end:0}}else s=null;for(Wa={focusedElem:t,selectionRange:s},Ks=!1,re=n;re!==null;)if(n=re,t=n.child,(n.subtreeFlags&1028)!==0&&t!==null)t.return=n,re=t;else for(;re!==null;){n=re;try{var ie=n.alternate;if((n.flags&1024)!==0)switch(n.tag){case 0:case 11:case 15:break;case 1:if(ie!==null){var ae=ie.memoizedProps,st=ie.memoizedState,I=n.stateNode,k=I.getSnapshotBeforeUpdate(n.elementType===n.type?ae:Sn(n.type,ae),st);I.__reactInternalSnapshotBeforeUpdate=k}break;case 3:var N=n.stateNode.containerInfo;N.nodeType===1?N.textContent="":N.nodeType===9&&N.documentElement&&N.removeChild(N.documentElement);break;case 5:case 6:case 4:case 17:break;default:throw Error(r(163))}}catch(X){rt(n,n.return,X)}if(t=n.sibling,t!==null){t.return=n.return,re=t;break}re=n.return}return ie=Wd,Wd=!1,ie}function Es(t,n,s){var a=n.updateQueue;if(a=a!==null?a.lastEffect:null,a!==null){var u=a=a.next;do{if((u.tag&t)===t){var d=u.destroy;u.destroy=void 0,d!==void 0&&Ml(n,s,d)}u=u.next}while(u!==a)}}function Po(t,n){if(n=n.updateQueue,n=n!==null?n.lastEffect:null,n!==null){var s=n=n.next;do{if((s.tag&t)===t){var a=s.create;s.destroy=a()}s=s.next}while(s!==n)}}function Dl(t){var n=t.ref;if(n!==null){var s=t.stateNode;switch(t.tag){case 5:t=s;break;default:t=s}typeof n=="function"?n(t):n.current=t}}function Gd(t){var n=t.alternate;n!==null&&(t.alternate=null,Gd(n)),t.child=null,t.deletions=null,t.sibling=null,t.tag===5&&(n=t.stateNode,n!==null&&(delete n[Ln],delete n[ds],delete n[Xa],delete n[dg],delete n[hg])),t.stateNode=null,t.return=null,t.dependencies=null,t.memoizedProps=null,t.memoizedState=null,t.pendingProps=null,t.stateNode=null,t.updateQueue=null}function qd(t){return t.tag===5||t.tag===3||t.tag===4}function Kd(t){e:for(;;){for(;t.sibling===null;){if(t.return===null||qd(t.return))return null;t=t.return}for(t.sibling.return=t.return,t=t.sibling;t.tag!==5&&t.tag!==6&&t.tag!==18;){if(t.flags&2||t.child===null||t.tag===4)continue e;t.child.return=t,t=t.child}if(!(t.flags&2))return t.stateNode}}function bl(t,n,s){var a=t.tag;if(a===5||a===6)t=t.stateNode,n?s.nodeType===8?s.parentNode.insertBefore(t,n):s.insertBefore(t,n):(s.nodeType===8?(n=s.parentNode,n.insertBefore(t,s)):(n=s,n.appendChild(t)),s=s._reactRootContainer,s!=null||n.onclick!==null||(n.onclick=oo));else if(a!==4&&(t=t.child,t!==null))for(bl(t,n,s),t=t.sibling;t!==null;)bl(t,n,s),t=t.sibling}function Ll(t,n,s){var a=t.tag;if(a===5||a===6)t=t.stateNode,n?s.insertBefore(t,n):s.appendChild(t);else if(a!==4&&(t=t.child,t!==null))for(Ll(t,n,s),t=t.sibling;t!==null;)Ll(t,n,s),t=t.sibling}var xt=null,kn=!1;function Ir(t,n,s){for(s=s.child;s!==null;)Xd(t,n,s),s=s.sibling}function Xd(t,n,s){if(Jt&&typeof Jt.onCommitFiberUnmount=="function")try{Jt.onCommitFiberUnmount(wn,s)}catch{}switch(s.tag){case 5:Rt||Di(s,n);case 6:var a=xt,u=kn;xt=null,Ir(t,n,s),xt=a,kn=u,xt!==null&&(kn?(t=xt,s=s.stateNode,t.nodeType===8?t.parentNode.removeChild(s):t.removeChild(s)):xt.removeChild(s.stateNode));break;case 18:xt!==null&&(kn?(t=xt,s=s.stateNode,t.nodeType===8?Ka(t.parentNode,s):t.nodeType===1&&Ka(t,s),es(t)):Ka(xt,s.stateNode));break;case 4:a=xt,u=kn,xt=s.stateNode.containerInfo,kn=!0,Ir(t,n,s),xt=a,kn=u;break;case 0:case 11:case 14:case 15:if(!Rt&&(a=s.updateQueue,a!==null&&(a=a.lastEffect,a!==null))){u=a=a.next;do{var d=u,p=d.destroy;d=d.tag,p!==void 0&&((d&2)!==0||(d&4)!==0)&&Ml(s,n,p),u=u.next}while(u!==a)}Ir(t,n,s);break;case 1:if(!Rt&&(Di(s,n),a=s.stateNode,typeof a.componentWillUnmount=="function"))try{a.props=s.memoizedProps,a.state=s.memoizedState,a.componentWillUnmount()}catch(y){rt(s,n,y)}Ir(t,n,s);break;case 21:Ir(t,n,s);break;case 22:s.mode&1?(Rt=(a=Rt)||s.memoizedState!==null,Ir(t,n,s),Rt=a):Ir(t,n,s);break;default:Ir(t,n,s)}}function Yd(t){var n=t.updateQueue;if(n!==null){t.updateQueue=null;var s=t.stateNode;s===null&&(s=t.stateNode=new Rg),n.forEach(function(a){var u=zg.bind(null,t,a);s.has(a)||(s.add(a),a.then(u,u))})}}function Tn(t,n){var s=n.deletions;if(s!==null)for(var a=0;a<s.length;a++){var u=s[a];try{var d=t,p=n,y=p;e:for(;y!==null;){switch(y.tag){case 5:xt=y.stateNode,kn=!1;break e;case 3:xt=y.stateNode.containerInfo,kn=!0;break e;case 4:xt=y.stateNode.containerInfo,kn=!0;break e}y=y.return}if(xt===null)throw Error(r(160));Xd(d,p,u),xt=null,kn=!1;var _=u.alternate;_!==null&&(_.return=null),u.return=null}catch(M){rt(u,n,M)}}if(n.subtreeFlags&12854)for(n=n.child;n!==null;)Qd(n,t),n=n.sibling}function Qd(t,n){var s=t.alternate,a=t.flags;switch(t.tag){case 0:case 11:case 14:case 15:if(Tn(n,t),zn(t),a&4){try{Es(3,t,t.return),Po(3,t)}catch(ae){rt(t,t.return,ae)}try{Es(5,t,t.return)}catch(ae){rt(t,t.return,ae)}}break;case 1:Tn(n,t),zn(t),a&512&&s!==null&&Di(s,s.return);break;case 5:if(Tn(n,t),zn(t),a&512&&s!==null&&Di(s,s.return),t.flags&32){var u=t.stateNode;try{Ft(u,"")}catch(ae){rt(t,t.return,ae)}}if(a&4&&(u=t.stateNode,u!=null)){var d=t.memoizedProps,p=s!==null?s.memoizedProps:d,y=t.type,_=t.updateQueue;if(t.updateQueue=null,_!==null)try{y==="input"&&d.type==="radio"&&d.name!=null&&vt(u,d),J(y,p);var M=J(y,d);for(p=0;p<_.length;p+=2){var U=_[p],$=_[p+1];U==="style"?G(u,$):U==="dangerouslySetInnerHTML"?Kt(u,$):U==="children"?Ft(u,$):q(u,U,$,M)}switch(y){case"input":qt(u,d);break;case"textarea":Wn(u,d);break;case"select":var z=u._wrapperState.wasMultiple;u._wrapperState.wasMultiple=!!d.multiple;var Z=d.value;Z!=null?Fe(u,!!d.multiple,Z,!1):z!==!!d.multiple&&(d.defaultValue!=null?Fe(u,!!d.multiple,d.defaultValue,!0):Fe(u,!!d.multiple,d.multiple?[]:"",!1))}u[ds]=d}catch(ae){rt(t,t.return,ae)}}break;case 6:if(Tn(n,t),zn(t),a&4){if(t.stateNode===null)throw Error(r(162));u=t.stateNode,d=t.memoizedProps;try{u.nodeValue=d}catch(ae){rt(t,t.return,ae)}}break;case 3:if(Tn(n,t),zn(t),a&4&&s!==null&&s.memoizedState.isDehydrated)try{es(n.containerInfo)}catch(ae){rt(t,t.return,ae)}break;case 4:Tn(n,t),zn(t);break;case 13:Tn(n,t),zn(t),u=t.child,u.flags&8192&&(d=u.memoizedState!==null,u.stateNode.isHidden=d,!d||u.alternate!==null&&u.alternate.memoizedState!==null||(zl=Ge())),a&4&&Yd(t);break;case 22:if(U=s!==null&&s.memoizedState!==null,t.mode&1?(Rt=(M=Rt)||U,Tn(n,t),Rt=M):Tn(n,t),zn(t),a&8192){if(M=t.memoizedState!==null,(t.stateNode.isHidden=M)&&!U&&(t.mode&1)!==0)for(re=t,U=t.child;U!==null;){for($=re=U;re!==null;){switch(z=re,Z=z.child,z.tag){case 0:case 11:case 14:case 15:Es(4,z,z.return);break;case 1:Di(z,z.return);var ie=z.stateNode;if(typeof ie.componentWillUnmount=="function"){a=z,s=z.return;try{n=a,ie.props=n.memoizedProps,ie.state=n.memoizedState,ie.componentWillUnmount()}catch(ae){rt(a,s,ae)}}break;case 5:Di(z,z.return);break;case 22:if(z.memoizedState!==null){eh($);continue}}Z!==null?(Z.return=z,re=Z):eh($)}U=U.sibling}e:for(U=null,$=t;;){if($.tag===5){if(U===null){U=$;try{u=$.stateNode,M?(d=u.style,typeof d.setProperty=="function"?d.setProperty("display","none","important"):d.display="none"):(y=$.stateNode,_=$.memoizedProps.style,p=_!=null&&_.hasOwnProperty("display")?_.display:null,y.style.display=L("display",p))}catch(ae){rt(t,t.return,ae)}}}else if($.tag===6){if(U===null)try{$.stateNode.nodeValue=M?"":$.memoizedProps}catch(ae){rt(t,t.return,ae)}}else if(($.tag!==22&&$.tag!==23||$.memoizedState===null||$===t)&&$.child!==null){$.child.return=$,$=$.child;continue}if($===t)break e;for(;$.sibling===null;){if($.return===null||$.return===t)break e;U===$&&(U=null),$=$.return}U===$&&(U=null),$.sibling.return=$.return,$=$.sibling}}break;case 19:Tn(n,t),zn(t),a&4&&Yd(t);break;case 21:break;default:Tn(n,t),zn(t)}}function zn(t){var n=t.flags;if(n&2){try{e:{for(var s=t.return;s!==null;){if(qd(s)){var a=s;break e}s=s.return}throw Error(r(160))}switch(a.tag){case 5:var u=a.stateNode;a.flags&32&&(Ft(u,""),a.flags&=-33);var d=Kd(t);Ll(t,d,u);break;case 3:case 4:var p=a.stateNode.containerInfo,y=Kd(t);bl(t,y,p);break;default:throw Error(r(161))}}catch(_){rt(t,t.return,_)}t.flags&=-3}n&4096&&(t.flags&=-4097)}function Pg(t,n,s){re=t,Jd(t)}function Jd(t,n,s){for(var a=(t.mode&1)!==0;re!==null;){var u=re,d=u.child;if(u.tag===22&&a){var p=u.memoizedState!==null||No;if(!p){var y=u.alternate,_=y!==null&&y.memoizedState!==null||Rt;y=No;var M=Rt;if(No=p,(Rt=_)&&!M)for(re=u;re!==null;)p=re,_=p.child,p.tag===22&&p.memoizedState!==null?th(u):_!==null?(_.return=p,re=_):th(u);for(;d!==null;)re=d,Jd(d),d=d.sibling;re=u,No=y,Rt=M}Zd(t)}else(u.subtreeFlags&8772)!==0&&d!==null?(d.return=u,re=d):Zd(t)}}function Zd(t){for(;re!==null;){var n=re;if((n.flags&8772)!==0){var s=n.alternate;try{if((n.flags&8772)!==0)switch(n.tag){case 0:case 11:case 15:Rt||Po(5,n);break;case 1:var a=n.stateNode;if(n.flags&4&&!Rt)if(s===null)a.componentDidMount();else{var u=n.elementType===n.type?s.memoizedProps:Sn(n.type,s.memoizedProps);a.componentDidUpdate(u,s.memoizedState,a.__reactInternalSnapshotBeforeUpdate)}var d=n.updateQueue;d!==null&&ed(n,d,a);break;case 3:var p=n.updateQueue;if(p!==null){if(s=null,n.child!==null)switch(n.child.tag){case 5:s=n.child.stateNode;break;case 1:s=n.child.stateNode}ed(n,p,s)}break;case 5:var y=n.stateNode;if(s===null&&n.flags&4){s=y;var _=n.memoizedProps;switch(n.type){case"button":case"input":case"select":case"textarea":_.autoFocus&&s.focus();break;case"img":_.src&&(s.src=_.src)}}break;case 6:break;case 4:break;case 12:break;case 13:if(n.memoizedState===null){var M=n.alternate;if(M!==null){var U=M.memoizedState;if(U!==null){var $=U.dehydrated;$!==null&&es($)}}}break;case 19:case 17:case 21:case 22:case 23:case 25:break;default:throw Error(r(163))}Rt||n.flags&512&&Dl(n)}catch(z){rt(n,n.return,z)}}if(n===t){re=null;break}if(s=n.sibling,s!==null){s.return=n.return,re=s;break}re=n.return}}function eh(t){for(;re!==null;){var n=re;if(n===t){re=null;break}var s=n.sibling;if(s!==null){s.return=n.return,re=s;break}re=n.return}}function th(t){for(;re!==null;){var n=re;try{switch(n.tag){case 0:case 11:case 15:var s=n.return;try{Po(4,n)}catch(_){rt(n,s,_)}break;case 1:var a=n.stateNode;if(typeof a.componentDidMount=="function"){var u=n.return;try{a.componentDidMount()}catch(_){rt(n,u,_)}}var d=n.return;try{Dl(n)}catch(_){rt(n,d,_)}break;case 5:var p=n.return;try{Dl(n)}catch(_){rt(n,p,_)}}}catch(_){rt(n,n.return,_)}if(n===t){re=null;break}var y=n.sibling;if(y!==null){y.return=n.return,re=y;break}re=n.return}}var Ag=Math.ceil,Ao=B.ReactCurrentDispatcher,Ol=B.ReactCurrentOwner,mn=B.ReactCurrentBatchConfig,ze=0,mt=null,ut=null,_t=0,nn=0,bi=Er(0),ht=0,Ss=null,Zr=0,Mo=0,Fl=0,ks=null,Ht=null,zl=0,Li=1/0,nr=null,Do=!1,jl=null,Rr=null,bo=!1,Nr=null,Lo=0,Ts=0,Ul=null,Oo=-1,Fo=0;function Dt(){return(ze&6)!==0?Ge():Oo!==-1?Oo:Oo=Ge()}function Pr(t){return(t.mode&1)===0?1:(ze&2)!==0&&_t!==0?_t&-_t:pg.transition!==null?(Fo===0&&(Fo=Ut()),Fo):(t=$e,t!==0||(t=window.event,t=t===void 0?16:rc(t.type)),t)}function Cn(t,n,s,a){if(50<Ts)throw Ts=0,Ul=null,Error(r(185));Wr(t,s,a),((ze&2)===0||t!==mt)&&(t===mt&&((ze&2)===0&&(Mo|=s),ht===4&&Ar(t,_t)),Wt(t,a),s===1&&ze===0&&(n.mode&1)===0&&(Li=Ge()+500,co&&kr()))}function Wt(t,n){var s=t.callbackNode;Ki(t,n);var a=Hr(t,t===mt?_t:0);if(a===0)s!==null&&di(s),t.callbackNode=null,t.callbackPriority=0;else if(n=a&-a,t.callbackPriority!==n){if(s!=null&&di(s),n===1)t.tag===0?fg(rh.bind(null,t)):$c(rh.bind(null,t)),ug(function(){(ze&6)===0&&kr()}),s=null;else{switch(Xu(a)){case 1:s=Gi;break;case 4:s=fi;break;case 16:s=pi;break;case 536870912:s=qn;break;default:s=pi}s=dh(s,nh.bind(null,t))}t.callbackPriority=n,t.callbackNode=s}}function nh(t,n){if(Oo=-1,Fo=0,(ze&6)!==0)throw Error(r(327));var s=t.callbackNode;if(Oi()&&t.callbackNode!==s)return null;var a=Hr(t,t===mt?_t:0);if(a===0)return null;if((a&30)!==0||(a&t.expiredLanes)!==0||n)n=zo(t,a);else{n=a;var u=ze;ze|=2;var d=sh();(mt!==t||_t!==n)&&(nr=null,Li=Ge()+500,ti(t,n));do try{bg();break}catch(y){ih(t,y)}while(!0);il(),Ao.current=d,ze=u,ut!==null?n=0:(mt=null,_t=0,n=ht)}if(n!==0){if(n===2&&(u=Xi(t),u!==0&&(a=u,n=Bl(t,u))),n===1)throw s=Ss,ti(t,0),Ar(t,a),Wt(t,Ge()),s;if(n===6)Ar(t,a);else{if(u=t.current.alternate,(a&30)===0&&!Mg(u)&&(n=zo(t,a),n===2&&(d=Xi(t),d!==0&&(a=d,n=Bl(t,d))),n===1))throw s=Ss,ti(t,0),Ar(t,a),Wt(t,Ge()),s;switch(t.finishedWork=u,t.finishedLanes=a,n){case 0:case 1:throw Error(r(345));case 2:ni(t,Ht,nr);break;case 3:if(Ar(t,a),(a&130023424)===a&&(n=zl+500-Ge(),10<n)){if(Hr(t,0)!==0)break;if(u=t.suspendedLanes,(u&a)!==a){Dt(),t.pingedLanes|=t.suspendedLanes&u;break}t.timeoutHandle=qa(ni.bind(null,t,Ht,nr),n);break}ni(t,Ht,nr);break;case 4:if(Ar(t,a),(a&4194240)===a)break;for(n=t.eventTimes,u=-1;0<a;){var p=31-jt(a);d=1<<p,p=n[p],p>u&&(u=p),a&=~d}if(a=u,a=Ge()-a,a=(120>a?120:480>a?480:1080>a?1080:1920>a?1920:3e3>a?3e3:4320>a?4320:1960*Ag(a/1960))-a,10<a){t.timeoutHandle=qa(ni.bind(null,t,Ht,nr),a);break}ni(t,Ht,nr);break;case 5:ni(t,Ht,nr);break;default:throw Error(r(329))}}}return Wt(t,Ge()),t.callbackNode===s?nh.bind(null,t):null}function Bl(t,n){var s=ks;return t.current.memoizedState.isDehydrated&&(ti(t,n).flags|=256),t=zo(t,n),t!==2&&(n=Ht,Ht=s,n!==null&&$l(n)),t}function $l(t){Ht===null?Ht=t:Ht.push.apply(Ht,t)}function Mg(t){for(var n=t;;){if(n.flags&16384){var s=n.updateQueue;if(s!==null&&(s=s.stores,s!==null))for(var a=0;a<s.length;a++){var u=s[a],d=u.getSnapshot;u=u.value;try{if(!_n(d(),u))return!1}catch{return!1}}}if(s=n.child,n.subtreeFlags&16384&&s!==null)s.return=n,n=s;else{if(n===t)break;for(;n.sibling===null;){if(n.return===null||n.return===t)return!0;n=n.return}n.sibling.return=n.return,n=n.sibling}}return!0}function Ar(t,n){for(n&=~Fl,n&=~Mo,t.suspendedLanes|=n,t.pingedLanes&=~n,t=t.expirationTimes;0<n;){var s=31-jt(n),a=1<<s;t[s]=-1,n&=~a}}function rh(t){if((ze&6)!==0)throw Error(r(327));Oi();var n=Hr(t,0);if((n&1)===0)return Wt(t,Ge()),null;var s=zo(t,n);if(t.tag!==0&&s===2){var a=Xi(t);a!==0&&(n=a,s=Bl(t,a))}if(s===1)throw s=Ss,ti(t,0),Ar(t,n),Wt(t,Ge()),s;if(s===6)throw Error(r(345));return t.finishedWork=t.current.alternate,t.finishedLanes=n,ni(t,Ht,nr),Wt(t,Ge()),null}function Vl(t,n){var s=ze;ze|=1;try{return t(n)}finally{ze=s,ze===0&&(Li=Ge()+500,co&&kr())}}function ei(t){Nr!==null&&Nr.tag===0&&(ze&6)===0&&Oi();var n=ze;ze|=1;var s=mn.transition,a=$e;try{if(mn.transition=null,$e=1,t)return t()}finally{$e=a,mn.transition=s,ze=n,(ze&6)===0&&kr()}}function Hl(){nn=bi.current,Xe(bi)}function ti(t,n){t.finishedWork=null,t.finishedLanes=0;var s=t.timeoutHandle;if(s!==-1&&(t.timeoutHandle=-1,lg(s)),ut!==null)for(s=ut.return;s!==null;){var a=s;switch(Za(a),a.tag){case 1:a=a.type.childContextTypes,a!=null&&lo();break;case 3:Ai(),Xe(Bt),Xe(Tt),hl();break;case 5:cl(a);break;case 4:Ai();break;case 13:Xe(Ze);break;case 19:Xe(Ze);break;case 10:sl(a.type._context);break;case 22:case 23:Hl()}s=s.return}if(mt=t,ut=t=Mr(t.current,null),_t=nn=n,ht=0,Ss=null,Fl=Mo=Zr=0,Ht=ks=null,Yr!==null){for(n=0;n<Yr.length;n++)if(s=Yr[n],a=s.interleaved,a!==null){s.interleaved=null;var u=a.next,d=s.pending;if(d!==null){var p=d.next;d.next=u,a.next=p}s.pending=a}Yr=null}return t}function ih(t,n){do{var s=ut;try{if(il(),_o.current=To,Eo){for(var a=et.memoizedState;a!==null;){var u=a.queue;u!==null&&(u.pending=null),a=a.next}Eo=!1}if(Jr=0,pt=dt=et=null,vs=!1,ys=0,Ol.current=null,s===null||s.return===null){ht=1,Ss=n,ut=null;break}e:{var d=t,p=s.return,y=s,_=n;if(n=_t,y.flags|=32768,_!==null&&typeof _=="object"&&typeof _.then=="function"){var M=_,U=y,$=U.tag;if((U.mode&1)===0&&($===0||$===11||$===15)){var z=U.alternate;z?(U.updateQueue=z.updateQueue,U.memoizedState=z.memoizedState,U.lanes=z.lanes):(U.updateQueue=null,U.memoizedState=null)}var Z=Nd(p);if(Z!==null){Z.flags&=-257,Pd(Z,p,y,d,n),Z.mode&1&&Rd(d,M,n),n=Z,_=M;var ie=n.updateQueue;if(ie===null){var ae=new Set;ae.add(_),n.updateQueue=ae}else ie.add(_);break e}else{if((n&1)===0){Rd(d,M,n),Wl();break e}_=Error(r(426))}}else if(Je&&y.mode&1){var st=Nd(p);if(st!==null){(st.flags&65536)===0&&(st.flags|=256),Pd(st,p,y,d,n),nl(Mi(_,y));break e}}d=_=Mi(_,y),ht!==4&&(ht=2),ks===null?ks=[d]:ks.push(d),d=p;do{switch(d.tag){case 3:d.flags|=65536,n&=-n,d.lanes|=n;var I=Cd(d,_,n);Zc(d,I);break e;case 1:y=_;var k=d.type,N=d.stateNode;if((d.flags&128)===0&&(typeof k.getDerivedStateFromError=="function"||N!==null&&typeof N.componentDidCatch=="function"&&(Rr===null||!Rr.has(N)))){d.flags|=65536,n&=-n,d.lanes|=n;var X=Id(d,y,n);Zc(d,X);break e}}d=d.return}while(d!==null)}ah(s)}catch(le){n=le,ut===s&&s!==null&&(ut=s=s.return);continue}break}while(!0)}function sh(){var t=Ao.current;return Ao.current=To,t===null?To:t}function Wl(){(ht===0||ht===3||ht===2)&&(ht=4),mt===null||(Zr&268435455)===0&&(Mo&268435455)===0||Ar(mt,_t)}function zo(t,n){var s=ze;ze|=2;var a=sh();(mt!==t||_t!==n)&&(nr=null,ti(t,n));do try{Dg();break}catch(u){ih(t,u)}while(!0);if(il(),ze=s,Ao.current=a,ut!==null)throw Error(r(261));return mt=null,_t=0,ht}function Dg(){for(;ut!==null;)oh(ut)}function bg(){for(;ut!==null&&!Qt();)oh(ut)}function oh(t){var n=ch(t.alternate,t,nn);t.memoizedProps=t.pendingProps,n===null?ah(t):ut=n,Ol.current=null}function ah(t){var n=t;do{var s=n.alternate;if(t=n.return,(n.flags&32768)===0){if(s=Cg(s,n,nn),s!==null){ut=s;return}}else{if(s=Ig(s,n),s!==null){s.flags&=32767,ut=s;return}if(t!==null)t.flags|=32768,t.subtreeFlags=0,t.deletions=null;else{ht=6,ut=null;return}}if(n=n.sibling,n!==null){ut=n;return}ut=n=t}while(n!==null);ht===0&&(ht=5)}function ni(t,n,s){var a=$e,u=mn.transition;try{mn.transition=null,$e=1,Lg(t,n,s,a)}finally{mn.transition=u,$e=a}return null}function Lg(t,n,s,a){do Oi();while(Nr!==null);if((ze&6)!==0)throw Error(r(327));s=t.finishedWork;var u=t.finishedLanes;if(s===null)return null;if(t.finishedWork=null,t.finishedLanes=0,s===t.current)throw Error(r(177));t.callbackNode=null,t.callbackPriority=0;var d=s.lanes|s.childLanes;if(Kn(t,d),t===mt&&(ut=mt=null,_t=0),(s.subtreeFlags&2064)===0&&(s.flags&2064)===0||bo||(bo=!0,dh(pi,function(){return Oi(),null})),d=(s.flags&15990)!==0,(s.subtreeFlags&15990)!==0||d){d=mn.transition,mn.transition=null;var p=$e;$e=1;var y=ze;ze|=4,Ol.current=null,Ng(t,s),Qd(s,t),tg(Wa),Ks=!!Ha,Wa=Ha=null,t.current=s,Pg(s),fr(),ze=y,$e=p,mn.transition=d}else t.current=s;if(bo&&(bo=!1,Nr=t,Lo=u),d=t.pendingLanes,d===0&&(Rr=null),qi(s.stateNode),Wt(t,Ge()),n!==null)for(a=t.onRecoverableError,s=0;s<n.length;s++)u=n[s],a(u.value,{componentStack:u.stack,digest:u.digest});if(Do)throw Do=!1,t=jl,jl=null,t;return(Lo&1)!==0&&t.tag!==0&&Oi(),d=t.pendingLanes,(d&1)!==0?t===Ul?Ts++:(Ts=0,Ul=t):Ts=0,kr(),null}function Oi(){if(Nr!==null){var t=Xu(Lo),n=mn.transition,s=$e;try{if(mn.transition=null,$e=16>t?16:t,Nr===null)var a=!1;else{if(t=Nr,Nr=null,Lo=0,(ze&6)!==0)throw Error(r(331));var u=ze;for(ze|=4,re=t.current;re!==null;){var d=re,p=d.child;if((re.flags&16)!==0){var y=d.deletions;if(y!==null){for(var _=0;_<y.length;_++){var M=y[_];for(re=M;re!==null;){var U=re;switch(U.tag){case 0:case 11:case 15:Es(8,U,d)}var $=U.child;if($!==null)$.return=U,re=$;else for(;re!==null;){U=re;var z=U.sibling,Z=U.return;if(Gd(U),U===M){re=null;break}if(z!==null){z.return=Z,re=z;break}re=Z}}}var ie=d.alternate;if(ie!==null){var ae=ie.child;if(ae!==null){ie.child=null;do{var st=ae.sibling;ae.sibling=null,ae=st}while(ae!==null)}}re=d}}if((d.subtreeFlags&2064)!==0&&p!==null)p.return=d,re=p;else e:for(;re!==null;){if(d=re,(d.flags&2048)!==0)switch(d.tag){case 0:case 11:case 15:Es(9,d,d.return)}var I=d.sibling;if(I!==null){I.return=d.return,re=I;break e}re=d.return}}var k=t.current;for(re=k;re!==null;){p=re;var N=p.child;if((p.subtreeFlags&2064)!==0&&N!==null)N.return=p,re=N;else e:for(p=k;re!==null;){if(y=re,(y.flags&2048)!==0)try{switch(y.tag){case 0:case 11:case 15:Po(9,y)}}catch(le){rt(y,y.return,le)}if(y===p){re=null;break e}var X=y.sibling;if(X!==null){X.return=y.return,re=X;break e}re=y.return}}if(ze=u,kr(),Jt&&typeof Jt.onPostCommitFiberRoot=="function")try{Jt.onPostCommitFiberRoot(wn,t)}catch{}a=!0}return a}finally{$e=s,mn.transition=n}}return!1}function lh(t,n,s){n=Mi(s,n),n=Cd(t,n,1),t=Cr(t,n,1),n=Dt(),t!==null&&(Wr(t,1,n),Wt(t,n))}function rt(t,n,s){if(t.tag===3)lh(t,t,s);else for(;n!==null;){if(n.tag===3){lh(n,t,s);break}else if(n.tag===1){var a=n.stateNode;if(typeof n.type.getDerivedStateFromError=="function"||typeof a.componentDidCatch=="function"&&(Rr===null||!Rr.has(a))){t=Mi(s,t),t=Id(n,t,1),n=Cr(n,t,1),t=Dt(),n!==null&&(Wr(n,1,t),Wt(n,t));break}}n=n.return}}function Og(t,n,s){var a=t.pingCache;a!==null&&a.delete(n),n=Dt(),t.pingedLanes|=t.suspendedLanes&s,mt===t&&(_t&s)===s&&(ht===4||ht===3&&(_t&130023424)===_t&&500>Ge()-zl?ti(t,0):Fl|=s),Wt(t,n)}function uh(t,n){n===0&&((t.mode&1)===0?n=1:(n=Vr,Vr<<=1,(Vr&130023424)===0&&(Vr=4194304)));var s=Dt();t=Zn(t,n),t!==null&&(Wr(t,n,s),Wt(t,s))}function Fg(t){var n=t.memoizedState,s=0;n!==null&&(s=n.retryLane),uh(t,s)}function zg(t,n){var s=0;switch(t.tag){case 13:var a=t.stateNode,u=t.memoizedState;u!==null&&(s=u.retryLane);break;case 19:a=t.stateNode;break;default:throw Error(r(314))}a!==null&&a.delete(n),uh(t,s)}var ch;ch=function(t,n,s){if(t!==null)if(t.memoizedProps!==n.pendingProps||Bt.current)Vt=!0;else{if((t.lanes&s)===0&&(n.flags&128)===0)return Vt=!1,Tg(t,n,s);Vt=(t.flags&131072)!==0}else Vt=!1,Je&&(n.flags&1048576)!==0&&Vc(n,fo,n.index);switch(n.lanes=0,n.tag){case 2:var a=n.type;Ro(t,n),t=n.pendingProps;var u=ki(n,Tt.current);Pi(n,s),u=ml(null,n,a,t,u,s);var d=gl();return n.flags|=1,typeof u=="object"&&u!==null&&typeof u.render=="function"&&u.$$typeof===void 0?(n.tag=1,n.memoizedState=null,n.updateQueue=null,$t(a)?(d=!0,uo(n)):d=!1,n.memoizedState=u.state!==null&&u.state!==void 0?u.state:null,ll(n),u.updater=Co,n.stateNode=u,u._reactInternals=n,El(n,a,t,s),n=Cl(null,n,a,!0,d,s)):(n.tag=0,Je&&d&&Ja(n),Mt(null,n,u,s),n=n.child),n;case 16:a=n.elementType;e:{switch(Ro(t,n),t=n.pendingProps,u=a._init,a=u(a._payload),n.type=a,u=n.tag=Ug(a),t=Sn(a,t),u){case 0:n=Tl(null,n,a,t,s);break e;case 1:n=Od(null,n,a,t,s);break e;case 11:n=Ad(null,n,a,t,s);break e;case 14:n=Md(null,n,a,Sn(a.type,t),s);break e}throw Error(r(306,a,""))}return n;case 0:return a=n.type,u=n.pendingProps,u=n.elementType===a?u:Sn(a,u),Tl(t,n,a,u,s);case 1:return a=n.type,u=n.pendingProps,u=n.elementType===a?u:Sn(a,u),Od(t,n,a,u,s);case 3:e:{if(Fd(n),t===null)throw Error(r(387));a=n.pendingProps,d=n.memoizedState,u=d.element,Jc(t,n),wo(n,a,null,s);var p=n.memoizedState;if(a=p.element,d.isDehydrated)if(d={element:a,isDehydrated:!1,cache:p.cache,pendingSuspenseBoundaries:p.pendingSuspenseBoundaries,transitions:p.transitions},n.updateQueue.baseState=d,n.memoizedState=d,n.flags&256){u=Mi(Error(r(423)),n),n=zd(t,n,a,s,u);break e}else if(a!==u){u=Mi(Error(r(424)),n),n=zd(t,n,a,s,u);break e}else for(tn=_r(n.stateNode.containerInfo.firstChild),en=n,Je=!0,En=null,s=Yc(n,null,a,s),n.child=s;s;)s.flags=s.flags&-3|4096,s=s.sibling;else{if(Ii(),a===u){n=tr(t,n,s);break e}Mt(t,n,a,s)}n=n.child}return n;case 5:return td(n),t===null&&tl(n),a=n.type,u=n.pendingProps,d=t!==null?t.memoizedProps:null,p=u.children,Ga(a,u)?p=null:d!==null&&Ga(a,d)&&(n.flags|=32),Ld(t,n),Mt(t,n,p,s),n.child;case 6:return t===null&&tl(n),null;case 13:return jd(t,n,s);case 4:return ul(n,n.stateNode.containerInfo),a=n.pendingProps,t===null?n.child=Ri(n,null,a,s):Mt(t,n,a,s),n.child;case 11:return a=n.type,u=n.pendingProps,u=n.elementType===a?u:Sn(a,u),Ad(t,n,a,u,s);case 7:return Mt(t,n,n.pendingProps,s),n.child;case 8:return Mt(t,n,n.pendingProps.children,s),n.child;case 12:return Mt(t,n,n.pendingProps.children,s),n.child;case 10:e:{if(a=n.type._context,u=n.pendingProps,d=n.memoizedProps,p=u.value,qe(go,a._currentValue),a._currentValue=p,d!==null)if(_n(d.value,p)){if(d.children===u.children&&!Bt.current){n=tr(t,n,s);break e}}else for(d=n.child,d!==null&&(d.return=n);d!==null;){var y=d.dependencies;if(y!==null){p=d.child;for(var _=y.firstContext;_!==null;){if(_.context===a){if(d.tag===1){_=er(-1,s&-s),_.tag=2;var M=d.updateQueue;if(M!==null){M=M.shared;var U=M.pending;U===null?_.next=_:(_.next=U.next,U.next=_),M.pending=_}}d.lanes|=s,_=d.alternate,_!==null&&(_.lanes|=s),ol(d.return,s,n),y.lanes|=s;break}_=_.next}}else if(d.tag===10)p=d.type===n.type?null:d.child;else if(d.tag===18){if(p=d.return,p===null)throw Error(r(341));p.lanes|=s,y=p.alternate,y!==null&&(y.lanes|=s),ol(p,s,n),p=d.sibling}else p=d.child;if(p!==null)p.return=d;else for(p=d;p!==null;){if(p===n){p=null;break}if(d=p.sibling,d!==null){d.return=p.return,p=d;break}p=p.return}d=p}Mt(t,n,u.children,s),n=n.child}return n;case 9:return u=n.type,a=n.pendingProps.children,Pi(n,s),u=fn(u),a=a(u),n.flags|=1,Mt(t,n,a,s),n.child;case 14:return a=n.type,u=Sn(a,n.pendingProps),u=Sn(a.type,u),Md(t,n,a,u,s);case 15:return Dd(t,n,n.type,n.pendingProps,s);case 17:return a=n.type,u=n.pendingProps,u=n.elementType===a?u:Sn(a,u),Ro(t,n),n.tag=1,$t(a)?(t=!0,uo(n)):t=!1,Pi(n,s),kd(n,a,u),El(n,a,u,s),Cl(null,n,a,!0,t,s);case 19:return Bd(t,n,s);case 22:return bd(t,n,s)}throw Error(r(156,n.tag))};function dh(t,n){return Yt(t,n)}function jg(t,n,s,a){this.tag=t,this.key=s,this.sibling=this.child=this.return=this.stateNode=this.type=this.elementType=null,this.index=0,this.ref=null,this.pendingProps=n,this.dependencies=this.memoizedState=this.updateQueue=this.memoizedProps=null,this.mode=a,this.subtreeFlags=this.flags=0,this.deletions=null,this.childLanes=this.lanes=0,this.alternate=null}function gn(t,n,s,a){return new jg(t,n,s,a)}function Gl(t){return t=t.prototype,!(!t||!t.isReactComponent)}function Ug(t){if(typeof t=="function")return Gl(t)?1:0;if(t!=null){if(t=t.$$typeof,t===ye)return 11;if(t===Ve)return 14}return 2}function Mr(t,n){var s=t.alternate;return s===null?(s=gn(t.tag,n,t.key,t.mode),s.elementType=t.elementType,s.type=t.type,s.stateNode=t.stateNode,s.alternate=t,t.alternate=s):(s.pendingProps=n,s.type=t.type,s.flags=0,s.subtreeFlags=0,s.deletions=null),s.flags=t.flags&14680064,s.childLanes=t.childLanes,s.lanes=t.lanes,s.child=t.child,s.memoizedProps=t.memoizedProps,s.memoizedState=t.memoizedState,s.updateQueue=t.updateQueue,n=t.dependencies,s.dependencies=n===null?null:{lanes:n.lanes,firstContext:n.firstContext},s.sibling=t.sibling,s.index=t.index,s.ref=t.ref,s}function jo(t,n,s,a,u,d){var p=2;if(a=t,typeof t=="function")Gl(t)&&(p=1);else if(typeof t=="string")p=5;else e:switch(t){case pe:return ri(s.children,u,d,n);case de:p=8,u|=8;break;case w:return t=gn(12,s,n,u|2),t.elementType=w,t.lanes=d,t;case me:return t=gn(13,s,n,u),t.elementType=me,t.lanes=d,t;case ue:return t=gn(19,s,n,u),t.elementType=ue,t.lanes=d,t;case Ce:return Uo(s,u,d,n);default:if(typeof t=="object"&&t!==null)switch(t.$$typeof){case Ne:p=10;break e;case we:p=9;break e;case ye:p=11;break e;case Ve:p=14;break e;case Pe:p=16,a=null;break e}throw Error(r(130,t==null?t:typeof t,""))}return n=gn(p,s,n,u),n.elementType=t,n.type=a,n.lanes=d,n}function ri(t,n,s,a){return t=gn(7,t,a,n),t.lanes=s,t}function Uo(t,n,s,a){return t=gn(22,t,a,n),t.elementType=Ce,t.lanes=s,t.stateNode={isHidden:!1},t}function ql(t,n,s){return t=gn(6,t,null,n),t.lanes=s,t}function Kl(t,n,s){return n=gn(4,t.children!==null?t.children:[],t.key,n),n.lanes=s,n.stateNode={containerInfo:t.containerInfo,pendingChildren:null,implementation:t.implementation},n}function Bg(t,n,s,a,u){this.tag=n,this.containerInfo=t,this.finishedWork=this.pingCache=this.current=this.pendingChildren=null,this.timeoutHandle=-1,this.callbackNode=this.pendingContext=this.context=null,this.callbackPriority=0,this.eventTimes=ct(0),this.expirationTimes=ct(-1),this.entangledLanes=this.finishedLanes=this.mutableReadLanes=this.expiredLanes=this.pingedLanes=this.suspendedLanes=this.pendingLanes=0,this.entanglements=ct(0),this.identifierPrefix=a,this.onRecoverableError=u,this.mutableSourceEagerHydrationData=null}function Xl(t,n,s,a,u,d,p,y,_){return t=new Bg(t,n,s,y,_),n===1?(n=1,d===!0&&(n|=8)):n=0,d=gn(3,null,null,n),t.current=d,d.stateNode=t,d.memoizedState={element:a,isDehydrated:s,cache:null,transitions:null,pendingSuspenseBoundaries:null},ll(d),t}function $g(t,n,s){var a=3<arguments.length&&arguments[3]!==void 0?arguments[3]:null;return{$$typeof:Q,key:a==null?null:""+a,children:t,containerInfo:n,implementation:s}}function hh(t){if(!t)return Sr;t=t._reactInternals;e:{if(bn(t)!==t||t.tag!==1)throw Error(r(170));var n=t;do{switch(n.tag){case 3:n=n.stateNode.context;break e;case 1:if($t(n.type)){n=n.stateNode.__reactInternalMemoizedMergedChildContext;break e}}n=n.return}while(n!==null);throw Error(r(171))}if(t.tag===1){var s=t.type;if($t(s))return Uc(t,s,n)}return n}function fh(t,n,s,a,u,d,p,y,_){return t=Xl(s,a,!0,t,u,d,p,y,_),t.context=hh(null),s=t.current,a=Dt(),u=Pr(s),d=er(a,u),d.callback=n??null,Cr(s,d,u),t.current.lanes=u,Wr(t,u,a),Wt(t,a),t}function Bo(t,n,s,a){var u=n.current,d=Dt(),p=Pr(u);return s=hh(s),n.context===null?n.context=s:n.pendingContext=s,n=er(d,p),n.payload={element:t},a=a===void 0?null:a,a!==null&&(n.callback=a),t=Cr(u,n,p),t!==null&&(Cn(t,u,p,d),yo(t,u,p)),p}function $o(t){if(t=t.current,!t.child)return null;switch(t.child.tag){case 5:return t.child.stateNode;default:return t.child.stateNode}}function ph(t,n){if(t=t.memoizedState,t!==null&&t.dehydrated!==null){var s=t.retryLane;t.retryLane=s!==0&&s<n?s:n}}function Yl(t,n){ph(t,n),(t=t.alternate)&&ph(t,n)}function Vg(){return null}var mh=typeof reportError=="function"?reportError:function(t){console.error(t)};function Ql(t){this._internalRoot=t}Vo.prototype.render=Ql.prototype.render=function(t){var n=this._internalRoot;if(n===null)throw Error(r(409));Bo(t,n,null,null)},Vo.prototype.unmount=Ql.prototype.unmount=function(){var t=this._internalRoot;if(t!==null){this._internalRoot=null;var n=t.containerInfo;ei(function(){Bo(null,t,null,null)}),n[Xn]=null}};function Vo(t){this._internalRoot=t}Vo.prototype.unstable_scheduleHydration=function(t){if(t){var n=Ju();t={blockedOn:null,target:t,priority:n};for(var s=0;s<yr.length&&n!==0&&n<yr[s].priority;s++);yr.splice(s,0,t),s===0&&tc(t)}};function Jl(t){return!(!t||t.nodeType!==1&&t.nodeType!==9&&t.nodeType!==11)}function Ho(t){return!(!t||t.nodeType!==1&&t.nodeType!==9&&t.nodeType!==11&&(t.nodeType!==8||t.nodeValue!==" react-mount-point-unstable "))}function gh(){}function Hg(t,n,s,a,u){if(u){if(typeof a=="function"){var d=a;a=function(){var M=$o(p);d.call(M)}}var p=fh(n,a,t,0,null,!1,!1,"",gh);return t._reactRootContainer=p,t[Xn]=p.current,us(t.nodeType===8?t.parentNode:t),ei(),p}for(;u=t.lastChild;)t.removeChild(u);if(typeof a=="function"){var y=a;a=function(){var M=$o(_);y.call(M)}}var _=Xl(t,0,!1,null,null,!1,!1,"",gh);return t._reactRootContainer=_,t[Xn]=_.current,us(t.nodeType===8?t.parentNode:t),ei(function(){Bo(n,_,s,a)}),_}function Wo(t,n,s,a,u){var d=s._reactRootContainer;if(d){var p=d;if(typeof u=="function"){var y=u;u=function(){var _=$o(p);y.call(_)}}Bo(n,p,t,u)}else p=Hg(s,n,t,u,a);return $o(p)}Yu=function(t){switch(t.tag){case 3:var n=t.stateNode;if(n.current.memoizedState.isDehydrated){var s=pr(n.pendingLanes);s!==0&&(xn(n,s|1),Wt(n,Ge()),(ze&6)===0&&(Li=Ge()+500,kr()))}break;case 13:ei(function(){var a=Zn(t,1);if(a!==null){var u=Dt();Cn(a,t,1,u)}}),Yl(t,1)}},Sa=function(t){if(t.tag===13){var n=Zn(t,134217728);if(n!==null){var s=Dt();Cn(n,t,134217728,s)}Yl(t,134217728)}},Qu=function(t){if(t.tag===13){var n=Pr(t),s=Zn(t,n);if(s!==null){var a=Dt();Cn(s,t,n,a)}Yl(t,n)}},Ju=function(){return $e},Zu=function(t,n){var s=$e;try{return $e=t,n()}finally{$e=s}},De=function(t,n,s){switch(n){case"input":if(qt(t,s),n=s.name,s.type==="radio"&&n!=null){for(s=t;s.parentNode;)s=s.parentNode;for(s=s.querySelectorAll("input[name="+JSON.stringify(""+n)+'][type="radio"]'),n=0;n<s.length;n++){var a=s[n];if(a!==t&&a.form===t.form){var u=ao(a);if(!u)throw Error(r(90));nt(a),qt(a,u)}}}break;case"textarea":Wn(t,s);break;case"select":n=s.value,n!=null&&Fe(t,!!s.multiple,n,!1)}},Re=Vl,yt=ei;var Wg={usingClientEntryPoint:!1,Events:[hs,Ei,ao,he,_e,Vl]},Cs={findFiberByHostInstance:Gr,bundleType:0,version:"18.3.1",rendererPackageName:"react-dom"},Gg={bundleType:Cs.bundleType,version:Cs.version,rendererPackageName:Cs.rendererPackageName,rendererConfig:Cs.rendererConfig,overrideHookState:null,overrideHookStateDeletePath:null,overrideHookStateRenamePath:null,overrideProps:null,overridePropsDeletePath:null,overridePropsRenamePath:null,setErrorHandler:null,setSuspenseHandler:null,scheduleUpdate:null,currentDispatcherRef:B.ReactCurrentDispatcher,findHostInstanceByFiber:function(t){return t=Pt(t),t===null?null:t.stateNode},findFiberByHostInstance:Cs.findFiberByHostInstance||Vg,findHostInstancesForRefresh:null,scheduleRefresh:null,scheduleRoot:null,setRefreshHandler:null,getCurrentFiber:null,reconcilerVersion:"18.3.1-next-f1338f8080-20240426"};if(typeof __REACT_DEVTOOLS_GLOBAL_HOOK__<"u"){var Go=__REACT_DEVTOOLS_GLOBAL_HOOK__;if(!Go.isDisabled&&Go.supportsFiber)try{wn=Go.inject(Gg),Jt=Go}catch{}}return Gt.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED=Wg,Gt.createPortal=function(t,n){var s=2<arguments.length&&arguments[2]!==void 0?arguments[2]:null;if(!Jl(n))throw Error(r(200));return $g(t,n,null,s)},Gt.createRoot=function(t,n){if(!Jl(t))throw Error(r(299));var s=!1,a="",u=mh;return n!=null&&(n.unstable_strictMode===!0&&(s=!0),n.identifierPrefix!==void 0&&(a=n.identifierPrefix),n.onRecoverableError!==void 0&&(u=n.onRecoverableError)),n=Xl(t,1,!1,null,null,s,!1,a,u),t[Xn]=n.current,us(t.nodeType===8?t.parentNode:t),new Ql(n)},Gt.findDOMNode=function(t){if(t==null)return null;if(t.nodeType===1)return t;var n=t._reactInternals;if(n===void 0)throw typeof t.render=="function"?Error(r(188)):(t=Object.keys(t).join(","),Error(r(268,t)));return t=Pt(n),t=t===null?null:t.stateNode,t},Gt.flushSync=function(t){return ei(t)},Gt.hydrate=function(t,n,s){if(!Ho(n))throw Error(r(200));return Wo(null,t,n,!0,s)},Gt.hydrateRoot=function(t,n,s){if(!Jl(t))throw Error(r(405));var a=s!=null&&s.hydratedSources||null,u=!1,d="",p=mh;if(s!=null&&(s.unstable_strictMode===!0&&(u=!0),s.identifierPrefix!==void 0&&(d=s.identifierPrefix),s.onRecoverableError!==void 0&&(p=s.onRecoverableError)),n=fh(n,null,t,1,s??null,u,!1,d,p),t[Xn]=n.current,us(t),a)for(t=0;t<a.length;t++)s=a[t],u=s._getVersion,u=u(s._source),n.mutableSourceEagerHydrationData==null?n.mutableSourceEagerHydrationData=[s,u]:n.mutableSourceEagerHydrationData.push(s,u);return new Vo(n)},Gt.render=function(t,n,s){if(!Ho(n))throw Error(r(200));return Wo(null,t,n,!1,s)},Gt.unmountComponentAtNode=function(t){if(!Ho(t))throw Error(r(40));return t._reactRootContainer?(ei(function(){Wo(null,null,t,!1,function(){t._reactRootContainer=null,t[Xn]=null})}),!0):!1},Gt.unstable_batchedUpdates=Vl,Gt.unstable_renderSubtreeIntoContainer=function(t,n,s,a){if(!Ho(s))throw Error(r(200));if(t==null||t._reactInternals===void 0)throw Error(r(38));return Wo(t,n,s,!1,a)},Gt.version="18.3.1-next-f1338f8080-20240426",Gt}var kh;function t0(){if(kh)return tu.exports;kh=1;function i(){if(!(typeof __REACT_DEVTOOLS_GLOBAL_HOOK__>"u"||typeof __REACT_DEVTOOLS_GLOBAL_HOOK__.checkDCE!="function"))try{__REACT_DEVTOOLS_GLOBAL_HOOK__.checkDCE(i)}catch(e){console.error(e)}}return i(),tu.exports=e0(),tu.exports}var Th;function n0(){if(Th)return qo;Th=1;var i=t0();return qo.createRoot=i.createRoot,qo.hydrateRoot=i.hydrateRoot,qo}var r0=n0();const i0=Of(r0);/**
 * @license lucide-react v1.64.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const s0=i=>i==null?void 0:i.replace(/([a-z0-9])([A-Z])/g,"$1-$2").toLowerCase();/**
 * @license lucide-react v1.64.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */function o0(i,e,r=[]){if(e==null)throw new Error("[lucide]: iconNode is required when icon name is used");return{name:s0(i),size:24,node:e,...r.length>0?{aliases:r}:{}}}/**
 * @license lucide-react v1.64.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const a0=i=>{let e="",r=!1;for(const o of i){if(o==="-"||o==="_"||o<=" "){r=e.length>0;continue}e.length===0?e+=o.toLowerCase():e+=r?o.toUpperCase():o,r=!1}return e};/**
 * @license lucide-react v1.64.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const l0=i=>{const e=a0(i);return e.charAt(0).toUpperCase()+e.slice(1)};/**
 * @license lucide-react v1.64.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const Eu=(...i)=>i.filter((e,r,o)=>!!e&&e.trim()!==""&&o.indexOf(e)===r).join(" ").trim();/**
 * @license lucide-react v1.64.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const ii={xmlns:"http://www.w3.org/2000/svg",width:24,height:24,viewBox:"0 0 24 24",fill:"none",stroke:"currentColor","stroke-width":2,"stroke-linecap":"round","stroke-linejoin":"round"};/**
 * @license lucide-react v1.64.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */function iu(i){return i!=null}function u0(i,e={}){var T,R;const r=e.attributeNames??{},o=P=>r[P]??P,l=i.size??i.width??ii.width,c=i.size??i.height??ii.height,h=((T=i.aliases)==null?void 0:T.filter(P=>typeof P=="string"&&P.trim()!=="").map(P=>`lucide-${P}`))??[],m=[...i.name?[`lucide-${i.name}`]:[],...h],f=((R=e.className)==null?void 0:R.split(" ").filter(Boolean))??[],v=e.includeDefaultClasses===!1?Eu(...f):Eu("lucide",...m,...f),x=e.absoluteStrokeWidth?Number(e.strokeWidth??ii["stroke-width"])*Number(i.size??i.width??ii.width)/Number(e.size??e.width??ii.width):e.strokeWidth??ii["stroke-width"];return["svg",{...Object.entries(ii).reduce((P,[b,A])=>(P[o(b)]=A,P),{}),..."color"in e&&e.color&&{[o("stroke")]:e.color},..."size"in e&&iu(e.size)&&{[o("width")]:e.size,[o("height")]:e.size},..."width"in e&&iu(e.width)&&{[o("width")]:e.width},..."height"in e&&iu(e.height)&&{[o("height")]:e.height},[o("stroke-width")]:x,...v&&{[o("class")]:v},[o("viewBox")]:`0 0 ${l} ${c}`,...e.hasA11yProp===!1?{[o("aria-hidden")]:"true"}:{},..."attributes"in e&&e.attributes},i.node.map(P=>{const[b,A,F]=P,se=e.nonScalingStroke?{[o("vector-effect")]:"non-scaling-stroke",...A}:A;return F?[b,se,F]:[b,se]})]}/**
 * @license lucide-react v1.64.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */function c0(i,e={}){return u0(i,{...e,attributeNames:{...e.attributeNames,class:"className","stroke-width":"strokeWidth","stroke-linecap":"strokeLinecap","stroke-linejoin":"strokeLinejoin","vector-effect":"vectorEffect"}})}/**
 * @license lucide-react v1.64.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const d0=i=>{for(const e in i)if(e.startsWith("aria-")||e==="role"||e==="title")return!0;return!1},h0=ne.createContext({}),f0=()=>ne.useContext(h0),p0=ne.forwardRef(({color:i,size:e,width:r,height:o,strokeWidth:l,absoluteStrokeWidth:c,nonScalingStroke:h,className:m="",children:f,iconNode:v=[],icon:x={node:v,aliases:[],size:24},...S},T)=>{const{size:R=24,strokeWidth:P=2,absoluteStrokeWidth:b=!1,nonScalingStroke:A=!1,color:F="currentColor",className:se=""}=f0()??{},q=!!f||d0(S),[B,W,Q=[]]=c0(x,{color:i??F,width:r??e??R,height:o??e??R,strokeWidth:l??P,absoluteStrokeWidth:c??b,nonScalingStroke:h??A,className:Eu(se,m),hasA11yProp:q,attributes:S});return ne.createElement(B,{ref:T,...W},[...Q.map(([pe,de])=>ne.createElement(pe,de)),...Array.isArray(f)?f:[f]])});/**
 * @license lucide-react v1.64.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */function Ye(i,e=[],r=[]){const o=typeof i=="string"?o0(i,e,r):i,l=ne.forwardRef(({className:c,...h},m)=>ne.createElement(p0,{ref:m,icon:o,className:c,...h}));return o.name&&(l.displayName=l0(o.name)),l}/**
 * @license lucide-react v1.64.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const Ff={name:"arrow-up-right",size:24,node:[["path",{d:"M7 7h10v10",key:"1tivn9"}],["path",{d:"M7 17 17 7",key:"1vkiza"}]]};Ff.node;const su=Ye(Ff);/**
 * @license lucide-react v1.64.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const zf={name:"chart-no-axes-column",size:24,node:[["path",{d:"M5 21v-6",key:"1hz6c0"}],["path",{d:"M12 21V3",key:"1lcnhd"}],["path",{d:"M19 21V9",key:"unv183"}]],aliases:["bar-chart-2"]};zf.node;const Ch=Ye(zf);/**
 * @license lucide-react v1.64.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const jf={name:"check",size:24,node:[["path",{d:"M20 6 9 17l-5-5",key:"1gmf2c"}]]};jf.node;const m0=Ye(jf);/**
 * @license lucide-react v1.64.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const Uf={name:"chevron-down",size:24,node:[["path",{d:"m6 9 6 6 6-6",key:"qrunsl"}]]};Uf.node;const Ih=Ye(Uf);/**
 * @license lucide-react v1.64.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const Bf={name:"chevron-right",size:24,node:[["path",{d:"m9 18 6-6-6-6",key:"mthhwq"}]]};Bf.node;const g0=Ye(Bf);/**
 * @license lucide-react v1.64.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const $f={name:"copy",size:24,node:[["rect",{width:"14",height:"14",x:"8",y:"8",rx:"2",ry:"2",key:"17jyea"}],["path",{d:"M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2",key:"zix9uf"}]]};$f.node;const v0=Ye($f);/**
 * @license lucide-react v1.64.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const Vf={name:"eye-off",size:24,node:[["path",{d:"M10.733 5.076a10.744 10.744 0 0 1 11.205 6.575 1 1 0 0 1 0 .696 10.747 10.747 0 0 1-1.444 2.49",key:"ct8e1f"}],["path",{d:"M14.084 14.158a3 3 0 0 1-4.242-4.242",key:"151rxh"}],["path",{d:"M17.479 17.499a10.75 10.75 0 0 1-15.417-5.151 1 1 0 0 1 0-.696 10.75 10.75 0 0 1 4.446-5.143",key:"13bj9a"}],["path",{d:"m2 2 20 20",key:"1ooewy"}]]};Vf.node;const y0=Ye(Vf);/**
 * @license lucide-react v1.64.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const Hf={name:"eye",size:24,node:[["path",{d:"M2.062 12.348a1 1 0 0 1 0-.696 10.75 10.75 0 0 1 19.876 0 1 1 0 0 1 0 .696 10.75 10.75 0 0 1-19.876 0",key:"1nclc0"}],["circle",{cx:"12",cy:"12",r:"3",key:"1v7zrd"}]]};Hf.node;const w0=Ye(Hf);/**
 * @license lucide-react v1.64.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const Wf={name:"file-text",size:24,node:[["path",{d:"M6 22a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h8a2.4 2.4 0 0 1 1.704.706l3.588 3.588A2.4 2.4 0 0 1 20 8v12a2 2 0 0 1-2 2z",key:"1oefj6"}],["path",{d:"M14 2v5a1 1 0 0 0 1 1h5",key:"wfsgrz"}],["path",{d:"M10 9H8",key:"b1mrlr"}],["path",{d:"M16 13H8",key:"t4e002"}],["path",{d:"M16 17H8",key:"z1uh3a"}]]};Wf.node;const Rh=Ye(Wf);/**
 * @license lucide-react v1.64.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const Gf={name:"life-buoy",size:24,node:[["circle",{cx:"12",cy:"12",r:"10",key:"1mglay"}],["path",{d:"m4.93 4.93 4.24 4.24",key:"1ymg45"}],["path",{d:"m14.83 9.17 4.24-4.24",key:"1cb5xl"}],["path",{d:"m14.83 14.83 4.24 4.24",key:"q42g0n"}],["path",{d:"m9.17 14.83-4.24 4.24",key:"bqpfvv"}],["circle",{cx:"12",cy:"12",r:"4",key:"4exip2"}]]};Gf.node;const Ko=Ye(Gf);/**
 * @license lucide-react v1.64.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const qf={name:"loader-circle",size:24,node:[["path",{d:"M21 12a9 9 0 1 1-6.219-8.56",key:"13zald"}]],aliases:["loader-2"]};qf.node;const x0=Ye(qf);/**
 * @license lucide-react v1.64.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const Kf={name:"log-out",size:24,node:[["path",{d:"m16 17 5-5-5-5",key:"1bji2h"}],["path",{d:"M21 12H9",key:"dn1m92"}],["path",{d:"M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4",key:"1uf3rs"}]]};Kf.node;const Nh=Ye(Kf);/**
 * @license lucide-react v1.64.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const Xf={name:"menu",size:24,node:[["path",{d:"M4 5h16",key:"1tepv9"}],["path",{d:"M4 12h16",key:"1lakjw"}],["path",{d:"M4 19h16",key:"1djgab"}]]};Xf.node;const _0=Ye(Xf);/**
 * @license lucide-react v1.64.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const Yf={name:"message-square",size:24,node:[["path",{d:"M22 17a2 2 0 0 1-2 2H6.828a2 2 0 0 0-1.414.586l-2.202 2.202A.71.71 0 0 1 2 21.286V5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2z",key:"18887p"}]]};Yf.node;const E0=Ye(Yf);/**
 * @license lucide-react v1.64.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const Qf={name:"pin",size:24,node:[["path",{d:"M12 17v5",key:"bb1du9"}],["path",{d:"M9 10.76a2 2 0 0 1-1.11 1.79l-1.78.9A2 2 0 0 0 5 15.24V16a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-.76a2 2 0 0 0-1.11-1.79l-1.78-.9A2 2 0 0 1 15 10.76V7a1 1 0 0 1 1-1 2 2 0 0 0 0-4H8a2 2 0 0 0 0 4 1 1 0 0 1 1 1z",key:"1nkz8b"}]]};Qf.node;const Ph=Ye(Qf);/**
 * @license lucide-react v1.64.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const Jf={name:"plus",size:24,node:[["path",{d:"M5 12h14",key:"1ays0h"}],["path",{d:"M12 5v14",key:"s699le"}]]};Jf.node;const Xo=Ye(Jf);/**
 * @license lucide-react v1.64.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const Zf={name:"search",size:24,node:[["path",{d:"m21 21-4.34-4.34",key:"14j7rj"}],["circle",{cx:"11",cy:"11",r:"8",key:"4ej97u"}]]};Zf.node;const S0=Ye(Zf);/**
 * @license lucide-react v1.64.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const ep={name:"send",size:24,node:[["path",{d:"M14.536 21.686a.5.5 0 0 0 .937-.024l6.5-19a.496.496 0 0 0-.635-.635l-19 6.5a.5.5 0 0 0-.024.937l7.93 3.18a2 2 0 0 1 1.112 1.11z",key:"1ffxy3"}],["path",{d:"m21.854 2.147-10.94 10.939",key:"12cjpa"}]]};ep.node;const Ah=Ye(ep);/**
 * @license lucide-react v1.64.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const tp={name:"settings",size:24,node:[["path",{d:"M9.671 4.136a2.34 2.34 0 0 1 4.659 0 2.34 2.34 0 0 0 3.319 1.915 2.34 2.34 0 0 1 2.33 4.033 2.34 2.34 0 0 0 0 3.831 2.34 2.34 0 0 1-2.33 4.033 2.34 2.34 0 0 0-3.319 1.915 2.34 2.34 0 0 1-4.659 0 2.34 2.34 0 0 0-3.32-1.915 2.34 2.34 0 0 1-2.33-4.033 2.34 2.34 0 0 0 0-3.831A2.34 2.34 0 0 1 6.35 6.051a2.34 2.34 0 0 0 3.319-1.915",key:"1i5ecw"}],["circle",{cx:"12",cy:"12",r:"3",key:"1v7zrd"}]]};tp.node;const Mh=Ye(tp);/**
 * @license lucide-react v1.64.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const np={name:"sliders-vertical",size:24,node:[["path",{d:"M10 8h4",key:"1sr2af"}],["path",{d:"M12 21v-9",key:"17s77i"}],["path",{d:"M12 8V3",key:"13r4qs"}],["path",{d:"M17 16h4",key:"h1uq16"}],["path",{d:"M19 12V3",key:"o1uvq1"}],["path",{d:"M19 21v-5",key:"qua636"}],["path",{d:"M3 14h4",key:"bcjad9"}],["path",{d:"M5 10V3",key:"cb8scm"}],["path",{d:"M5 21v-7",key:"1w1uti"}]],aliases:["sliders"]};np.node;const Dh=Ye(np);/**
 * @license lucide-react v1.64.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const rp={name:"sparkles",size:24,node:[["path",{d:"M11.017 2.814a1 1 0 0 1 1.966 0l1.051 5.558a2 2 0 0 0 1.594 1.594l5.558 1.051a1 1 0 0 1 0 1.966l-5.558 1.051a2 2 0 0 0-1.594 1.594l-1.051 5.558a1 1 0 0 1-1.966 0l-1.051-5.558a2 2 0 0 0-1.594-1.594l-5.558-1.051a1 1 0 0 1 0-1.966l5.558-1.051a2 2 0 0 0 1.594-1.594z",key:"1s2grr"}],["path",{d:"M20 2v4",key:"1rf3ol"}],["path",{d:"M22 4h-4",key:"gwowj6"}],["circle",{cx:"4",cy:"20",r:"2",key:"6kqj1y"}]],aliases:["stars"]};rp.node;const ou=Ye(rp);/**
 * @license lucide-react v1.64.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const ip={name:"thumbs-down",size:24,node:[["path",{d:"M9 18.12 10 14H4.17a2 2 0 0 1-1.92-2.56l2.33-8A2 2 0 0 1 6.5 2H20a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2h-2.76a2 2 0 0 0-1.79 1.11L12 22a3.13 3.13 0 0 1-3-3.88Z",key:"m61m77"}],["path",{d:"M17 14V2",key:"8ymqnk"}]]};ip.node;const k0=Ye(ip);/**
 * @license lucide-react v1.64.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const sp={name:"thumbs-up",size:24,node:[["path",{d:"M15 5.88 14 10h5.83a2 2 0 0 1 1.92 2.56l-2.33 8A2 2 0 0 1 17.5 22H4a2 2 0 0 1-2-2v-8a2 2 0 0 1 2-2h2.76a2 2 0 0 0 1.79-1.11L12 2a3.13 3.13 0 0 1 3 3.88Z",key:"emmmcr"}],["path",{d:"M7 10v12",key:"1qc93n"}]]};sp.node;const T0=Ye(sp);/**
 * @license lucide-react v1.64.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const op={name:"trash",size:24,node:[["path",{d:"M10 11v6",key:"nco0om"}],["path",{d:"M14 11v6",key:"outv1u"}],["path",{d:"M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6",key:"miytrc"}],["path",{d:"M3 6h18",key:"d0wm0j"}],["path",{d:"M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2",key:"e791ji"}]],aliases:["trash-2"]};op.node;const C0=Ye(op);/**
 * @license lucide-react v1.64.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const ap={name:"x",size:24,node:[["path",{d:"M18 6 6 18",key:"1bl5f8"}],["path",{d:"m6 6 12 12",key:"d8bk6v"}]]};ap.node;const Yo=Ye(ap),I0=()=>{};var bh={};/**
 * @license
 * Copyright 2017 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */const lp=function(i){const e=[];let r=0;for(let o=0;o<i.length;o++){let l=i.charCodeAt(o);l<128?e[r++]=l:l<2048?(e[r++]=l>>6|192,e[r++]=l&63|128):(l&64512)===55296&&o+1<i.length&&(i.charCodeAt(o+1)&64512)===56320?(l=65536+((l&1023)<<10)+(i.charCodeAt(++o)&1023),e[r++]=l>>18|240,e[r++]=l>>12&63|128,e[r++]=l>>6&63|128,e[r++]=l&63|128):(e[r++]=l>>12|224,e[r++]=l>>6&63|128,e[r++]=l&63|128)}return e},R0=function(i){const e=[];let r=0,o=0;for(;r<i.length;){const l=i[r++];if(l<128)e[o++]=String.fromCharCode(l);else if(l>191&&l<224){const c=i[r++];e[o++]=String.fromCharCode((l&31)<<6|c&63)}else if(l>239&&l<365){const c=i[r++],h=i[r++],m=i[r++],f=((l&7)<<18|(c&63)<<12|(h&63)<<6|m&63)-65536;e[o++]=String.fromCharCode(55296+(f>>10)),e[o++]=String.fromCharCode(56320+(f&1023))}else{const c=i[r++],h=i[r++];e[o++]=String.fromCharCode((l&15)<<12|(c&63)<<6|h&63)}}return e.join("")},up={byteToCharMap_:null,charToByteMap_:null,byteToCharMapWebSafe_:null,charToByteMapWebSafe_:null,ENCODED_VALS_BASE:"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789",get ENCODED_VALS(){return this.ENCODED_VALS_BASE+"+/="},get ENCODED_VALS_WEBSAFE(){return this.ENCODED_VALS_BASE+"-_."},HAS_NATIVE_SUPPORT:typeof atob=="function",encodeByteArray(i,e){if(!Array.isArray(i))throw Error("encodeByteArray takes an array as a parameter");this.init_();const r=e?this.byteToCharMapWebSafe_:this.byteToCharMap_,o=[];for(let l=0;l<i.length;l+=3){const c=i[l],h=l+1<i.length,m=h?i[l+1]:0,f=l+2<i.length,v=f?i[l+2]:0,x=c>>2,S=(c&3)<<4|m>>4;let T=(m&15)<<2|v>>6,R=v&63;f||(R=64,h||(T=64)),o.push(r[x],r[S],r[T],r[R])}return o.join("")},encodeString(i,e){return this.HAS_NATIVE_SUPPORT&&!e?btoa(i):this.encodeByteArray(lp(i),e)},decodeString(i,e){return this.HAS_NATIVE_SUPPORT&&!e?atob(i):R0(this.decodeStringToByteArray(i,e))},decodeStringToByteArray(i,e){this.init_();const r=e?this.charToByteMapWebSafe_:this.charToByteMap_,o=[];for(let l=0;l<i.length;){const c=r[i.charAt(l++)],m=l<i.length?r[i.charAt(l)]:0;++l;const v=l<i.length?r[i.charAt(l)]:64;++l;const S=l<i.length?r[i.charAt(l)]:64;if(++l,c==null||m==null||v==null||S==null)throw new N0;const T=c<<2|m>>4;if(o.push(T),v!==64){const R=m<<4&240|v>>2;if(o.push(R),S!==64){const P=v<<6&192|S;o.push(P)}}}return o},init_(){if(!this.byteToCharMap_){this.byteToCharMap_={},this.charToByteMap_={},this.byteToCharMapWebSafe_={},this.charToByteMapWebSafe_={};for(let i=0;i<this.ENCODED_VALS.length;i++)this.byteToCharMap_[i]=this.ENCODED_VALS.charAt(i),this.charToByteMap_[this.byteToCharMap_[i]]=i,this.byteToCharMapWebSafe_[i]=this.ENCODED_VALS_WEBSAFE.charAt(i),this.charToByteMapWebSafe_[this.byteToCharMapWebSafe_[i]]=i,i>=this.ENCODED_VALS_BASE.length&&(this.charToByteMap_[this.ENCODED_VALS_WEBSAFE.charAt(i)]=i,this.charToByteMapWebSafe_[this.ENCODED_VALS.charAt(i)]=i)}}};class N0 extends Error{constructor(){super(...arguments),this.name="DecodeBase64StringError"}}const P0=function(i){const e=lp(i);return up.encodeByteArray(e,!0)},cp=function(i){return P0(i).replace(/\./g,"")},dp=function(i){try{return up.decodeString(i,!0)}catch(e){console.error("base64Decode failed: ",e)}return null};/**
 * @license
 * Copyright 2022 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */function A0(){if(typeof self<"u")return self;if(typeof window<"u")return window;if(typeof global<"u")return global;throw new Error("Unable to locate global object.")}/**
 * @license
 * Copyright 2022 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */const M0=()=>A0().__FIREBASE_DEFAULTS__,D0=()=>{if(typeof process>"u"||typeof bh>"u")return;const i=bh.__FIREBASE_DEFAULTS__;if(i)return JSON.parse(i)},b0=()=>{if(typeof document>"u")return;let i;try{i=document.cookie.match(/__FIREBASE_DEFAULTS__=([^;]+)/)}catch{return}const e=i&&dp(i[1]);return e&&JSON.parse(e)},bu=()=>{try{return I0()||M0()||D0()||b0()}catch(i){console.info(`Unable to get __FIREBASE_DEFAULTS__ due to: ${i}`);return}},L0=i=>{var e,r;return(r=(e=bu())==null?void 0:e.emulatorHosts)==null?void 0:r[i]},hp=()=>{var i;return(i=bu())==null?void 0:i.config},fp=i=>{var e;return(e=bu())==null?void 0:e[`_${i}`]};/**
 * @license
 * Copyright 2017 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */class pp{constructor(){this.reject=()=>{},this.resolve=()=>{},this.promise=new Promise((e,r)=>{this.resolve=e,this.reject=r})}wrapCallback(e){return(r,o)=>{r?this.reject(r):this.resolve(o),typeof e=="function"&&(this.promise.catch(()=>{}),e.length===1?e(r):e(r,o))}}}/**
 * @license
 * Copyright 2017 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */function Lt(){return typeof navigator<"u"&&typeof navigator.userAgent=="string"?navigator.userAgent:""}function O0(){return typeof window<"u"&&!!(window.cordova||window.phonegap||window.PhoneGap)&&/ios|iphone|ipod|ipad|android|blackberry|iemobile/i.test(Lt())}function F0(){return typeof navigator<"u"&&navigator.userAgent==="Cloudflare-Workers"}function z0(){const i=typeof chrome=="object"?chrome.runtime:typeof browser=="object"?browser.runtime:void 0;return typeof i=="object"&&i.id!==void 0}function j0(){return typeof navigator=="object"&&navigator.product==="ReactNative"}function U0(){const i=Lt();return i.indexOf("MSIE ")>=0||i.indexOf("Trident/")>=0}function B0(){try{return typeof indexedDB=="object"}catch{return!1}}function $0(){return new Promise((i,e)=>{try{let r=!0;const o="validate-browser-context-for-indexeddb-analytics-module",l=self.indexedDB.open(o);l.onsuccess=()=>{l.result.close(),r||self.indexedDB.deleteDatabase(o),i(!0)},l.onupgradeneeded=()=>{r=!1},l.onerror=()=>{var c;e(((c=l.error)==null?void 0:c.message)||"")}}catch(r){e(r)}})}/**
 * @license
 * Copyright 2017 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */const V0="FirebaseError";class Br extends Error{constructor(e,r,o){super(r),this.code=e,this.customData=o,this.name=V0,Object.setPrototypeOf(this,Br.prototype),Error.captureStackTrace&&Error.captureStackTrace(this,Fs.prototype.create)}}class Fs{constructor(e,r,o){this.service=e,this.serviceName=r,this.errors=o}create(e,...r){const o=r[0]||{},l=`${this.service}/${e}`,c=this.errors[e],h=c?H0(c,o):"Error",m=`${this.serviceName}: ${h} (${l}).`;return new Br(l,m,o)}}function H0(i,e){try{let r=0,o="";for(;r<i.length;){const l=i.indexOf("{$",r);if(l===-1){o+=i.substring(r);break}const c=i.indexOf("}",l+2);if(c===-1){o+=i.substring(r);break}const h=i.substring(l+2,c),m=e[h];o+=i.substring(r,l)+(m!=null?String(m):`<${h}?>`),r=c+1}return o}catch{return i}}function W0(i){for(const e in i)if(Object.prototype.hasOwnProperty.call(i,e))return!1;return!0}function $i(i,e){if(i===e)return!0;const r=Object.keys(i),o=Object.keys(e);for(const l of r){if(!o.includes(l))return!1;const c=i[l],h=e[l];if(Lh(c)&&Lh(h)){if(!$i(c,h))return!1}else if(c!==h)return!1}for(const l of o)if(!r.includes(l))return!1;return!0}function Lh(i){return i!==null&&typeof i=="object"}/**
 * @license
 * Copyright 2017 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */function zs(i){const e=[];for(const[r,o]of Object.entries(i))Array.isArray(o)?o.forEach(l=>{e.push(encodeURIComponent(r)+"="+encodeURIComponent(l))}):e.push(encodeURIComponent(r)+"="+encodeURIComponent(o));return e.length?"&"+e.join("&"):""}function Rs(i){const e={};return i.replace(/^\?/,"").split("&").forEach(o=>{if(o){const[l,c]=o.split("=");e[decodeURIComponent(l)]=decodeURIComponent(c)}}),e}function Ns(i){const e=i.indexOf("?");if(!e)return"";const r=i.indexOf("#",e);return i.substring(e,r>0?r:void 0)}function G0(i,e){const r=new q0(i,e);return r.subscribe.bind(r)}class q0{constructor(e,r){this.observers=[],this.unsubscribes=[],this.observerCount=0,this.task=Promise.resolve(),this.finalized=!1,this.onNoObservers=r,this.task.then(()=>{e(this)}).catch(o=>{this.error(o)})}next(e){this.forEachObserver(r=>{r.next(e)})}error(e){this.forEachObserver(r=>{r.error(e)}),this.close(e)}complete(){this.forEachObserver(e=>{e.complete()}),this.close()}subscribe(e,r,o){let l;if(e===void 0&&r===void 0&&o===void 0)throw new Error("Missing Observer.");K0(e,["next","error","complete"])?l=e:l={next:e,error:r,complete:o},l.next===void 0&&(l.next=au),l.error===void 0&&(l.error=au),l.complete===void 0&&(l.complete=au);const c=this.unsubscribeOne.bind(this,this.observers.length);return this.finalized&&this.task.then(()=>{try{this.finalError?l.error(this.finalError):l.complete()}catch{}}),this.observers.push(l),c}unsubscribeOne(e){this.observers===void 0||this.observers[e]===void 0||(delete this.observers[e],this.observerCount-=1,this.observerCount===0&&this.onNoObservers!==void 0&&this.onNoObservers(this))}forEachObserver(e){if(!this.finalized)for(let r=0;r<this.observers.length;r++)this.sendOne(r,e)}sendOne(e,r){this.task.then(()=>{if(this.observers!==void 0&&this.observers[e]!==void 0)try{r(this.observers[e])}catch(o){typeof console<"u"&&console.error&&console.error(o)}})}close(e){this.finalized||(this.finalized=!0,e!==void 0&&(this.finalError=e),this.task.then(()=>{this.observers=void 0,this.onNoObservers=void 0}))}}function K0(i,e){if(typeof i!="object"||i===null)return!1;for(const r of e)if(r in i&&typeof i[r]=="function")return!0;return!1}function au(){}/**
 * @license
 * Copyright 2021 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */function Bn(i){return i&&i._delegate?i._delegate:i}/**
 * @license
 * Copyright 2025 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */function Lu(i){try{return(i.startsWith("http://")||i.startsWith("https://")?new URL(i).hostname:i).endsWith(".cloudworkstations.dev")}catch{return!1}}async function X0(i){return(await fetch(i,{credentials:"include"})).ok}class Vi{constructor(e,r,o){this.name=e,this.instanceFactory=r,this.type=o,this.multipleInstances=!1,this.serviceProps={},this.instantiationMode="LAZY",this.onInstanceCreated=null}setInstantiationMode(e){return this.instantiationMode=e,this}setMultipleInstances(e){return this.multipleInstances=e,this}setServiceProps(e){return this.serviceProps=e,this}setInstanceCreatedCallback(e){return this.onInstanceCreated=e,this}}/**
 * @license
 * Copyright 2019 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */const oi="[DEFAULT]";/**
 * @license
 * Copyright 2019 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */class Y0{constructor(e,r){this.name=e,this.container=r,this.component=null,this.instances=new Map,this.instancesDeferred=new Map,this.instancesOptions=new Map,this.onInitCallbacks=new Map}get(e){const r=this.normalizeInstanceIdentifier(e);if(!this.instancesDeferred.has(r)){const o=new pp;if(this.instancesDeferred.set(r,o),this.isInitialized(r)||this.shouldAutoInitialize())try{const l=this.getOrInitializeService({instanceIdentifier:r});l&&o.resolve(l)}catch{}}return this.instancesDeferred.get(r).promise}getImmediate(e){const r=this.normalizeInstanceIdentifier(e==null?void 0:e.identifier),o=(e==null?void 0:e.optional)??!1;if(this.isInitialized(r)||this.shouldAutoInitialize())try{return this.getOrInitializeService({instanceIdentifier:r})}catch(l){if(o)return null;throw l}else{if(o)return null;throw Error(`Service ${this.name} is not available`)}}getComponent(){return this.component}setComponent(e){if(e.name!==this.name)throw Error(`Mismatching Component ${e.name} for Provider ${this.name}.`);if(this.component)throw Error(`Component for ${this.name} has already been provided`);if(this.component=e,!!this.shouldAutoInitialize()){if(J0(e))try{this.getOrInitializeService({instanceIdentifier:oi})}catch{}for(const[r,o]of this.instancesDeferred.entries()){const l=this.normalizeInstanceIdentifier(r);try{const c=this.getOrInitializeService({instanceIdentifier:l});o.resolve(c)}catch{}}}}clearInstance(e=oi){this.instancesDeferred.delete(e),this.instancesOptions.delete(e),this.instances.delete(e)}async delete(){const e=Array.from(this.instances.values());await Promise.all([...e.filter(r=>"INTERNAL"in r).map(r=>r.INTERNAL.delete()),...e.filter(r=>"_delete"in r).map(r=>r._delete())])}isComponentSet(){return this.component!=null}isInitialized(e=oi){return this.instances.has(e)}getOptions(e=oi){return this.instancesOptions.get(e)||{}}initialize(e={}){const{options:r={}}=e,o=this.normalizeInstanceIdentifier(e.instanceIdentifier);if(this.isInitialized(o))throw Error(`${this.name}(${o}) has already been initialized`);if(!this.isComponentSet())throw Error(`Component ${this.name} has not been registered yet`);const l=this.getOrInitializeService({instanceIdentifier:o,options:r});for(const[c,h]of this.instancesDeferred.entries()){const m=this.normalizeInstanceIdentifier(c);o===m&&h.resolve(l)}return l}onInit(e,r){const o=this.normalizeInstanceIdentifier(r),l=this.onInitCallbacks.get(o)??new Set;l.add(e),this.onInitCallbacks.set(o,l);const c=this.instances.get(o);return c&&e(c,o),()=>{l.delete(e)}}invokeOnInitCallbacks(e,r){const o=this.onInitCallbacks.get(r);if(o)for(const l of o)try{l(e,r)}catch{}}getOrInitializeService({instanceIdentifier:e,options:r={}}){let o=this.instances.get(e);if(!o&&this.component&&(o=this.component.instanceFactory(this.container,{instanceIdentifier:Q0(e),options:r}),this.instances.set(e,o),this.instancesOptions.set(e,r),this.invokeOnInitCallbacks(o,e),this.component.onInstanceCreated))try{this.component.onInstanceCreated(this.container,e,o)}catch{}return o||null}normalizeInstanceIdentifier(e=oi){return this.component?this.component.multipleInstances?e:oi:e}shouldAutoInitialize(){return!!this.component&&this.component.instantiationMode!=="EXPLICIT"}}function Q0(i){return i===oi?void 0:i}function J0(i){return i.instantiationMode==="EAGER"}/**
 * @license
 * Copyright 2019 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */class Z0{constructor(e){this.name=e,this.providers=new Map}addComponent(e){const r=this.getProvider(e.name);if(r.isComponentSet())throw new Error(`Component ${e.name} has already been registered with ${this.name}`);r.setComponent(e)}addOrOverwriteComponent(e){this.getProvider(e.name).isComponentSet()&&this.providers.delete(e.name),this.addComponent(e)}getProvider(e){if(this.providers.has(e))return this.providers.get(e);const r=new Y0(e,this);return this.providers.set(e,r),r}getProviders(){return Array.from(this.providers.values())}}/**
 * @license
 * Copyright 2017 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */var We;(function(i){i[i.DEBUG=0]="DEBUG",i[i.VERBOSE=1]="VERBOSE",i[i.INFO=2]="INFO",i[i.WARN=3]="WARN",i[i.ERROR=4]="ERROR",i[i.SILENT=5]="SILENT"})(We||(We={}));const ev={debug:We.DEBUG,verbose:We.VERBOSE,info:We.INFO,warn:We.WARN,error:We.ERROR,silent:We.SILENT},tv=We.INFO,nv={[We.DEBUG]:"log",[We.VERBOSE]:"log",[We.INFO]:"info",[We.WARN]:"warn",[We.ERROR]:"error"},rv=(i,e,...r)=>{if(e<i.logLevel)return;const o=new Date().toISOString(),l=nv[e];if(l)console[l](`[${o}]  ${i.name}:`,...r);else throw new Error(`Attempted to log a message with an invalid logType (value: ${e})`)};class mp{constructor(e){this.name=e,this._logLevel=tv,this._logHandler=rv,this._userLogHandler=null}get logLevel(){return this._logLevel}set logLevel(e){if(!(e in We))throw new TypeError(`Invalid value "${e}" assigned to \`logLevel\``);this._logLevel=e}setLogLevel(e){this._logLevel=typeof e=="string"?ev[e]:e}get logHandler(){return this._logHandler}set logHandler(e){if(typeof e!="function")throw new TypeError("Value assigned to `logHandler` must be a function");this._logHandler=e}get userLogHandler(){return this._userLogHandler}set userLogHandler(e){this._userLogHandler=e}debug(...e){this._userLogHandler&&this._userLogHandler(this,We.DEBUG,...e),this._logHandler(this,We.DEBUG,...e)}log(...e){this._userLogHandler&&this._userLogHandler(this,We.VERBOSE,...e),this._logHandler(this,We.VERBOSE,...e)}info(...e){this._userLogHandler&&this._userLogHandler(this,We.INFO,...e),this._logHandler(this,We.INFO,...e)}warn(...e){this._userLogHandler&&this._userLogHandler(this,We.WARN,...e),this._logHandler(this,We.WARN,...e)}error(...e){this._userLogHandler&&this._userLogHandler(this,We.ERROR,...e),this._logHandler(this,We.ERROR,...e)}}const iv=(i,e)=>e.some(r=>i instanceof r);let Oh,Fh;function sv(){return Oh||(Oh=[IDBDatabase,IDBObjectStore,IDBIndex,IDBCursor,IDBTransaction])}function ov(){return Fh||(Fh=[IDBCursor.prototype.advance,IDBCursor.prototype.continue,IDBCursor.prototype.continuePrimaryKey])}const gp=new WeakMap,Su=new WeakMap,vp=new WeakMap,lu=new WeakMap,Ou=new WeakMap;function av(i){const e=new Promise((r,o)=>{const l=()=>{i.removeEventListener("success",c),i.removeEventListener("error",h)},c=()=>{r(jr(i.result)),l()},h=()=>{o(i.error),l()};i.addEventListener("success",c),i.addEventListener("error",h)});return e.then(r=>{r instanceof IDBCursor&&gp.set(r,i)}).catch(()=>{}),Ou.set(e,i),e}function lv(i){if(Su.has(i))return;const e=new Promise((r,o)=>{const l=()=>{i.removeEventListener("complete",c),i.removeEventListener("error",h),i.removeEventListener("abort",h)},c=()=>{r(),l()},h=()=>{o(i.error||new DOMException("AbortError","AbortError")),l()};i.addEventListener("complete",c),i.addEventListener("error",h),i.addEventListener("abort",h)});Su.set(i,e)}let ku={get(i,e,r){if(i instanceof IDBTransaction){if(e==="done")return Su.get(i);if(e==="objectStoreNames")return i.objectStoreNames||vp.get(i);if(e==="store")return r.objectStoreNames[1]?void 0:r.objectStore(r.objectStoreNames[0])}return jr(i[e])},set(i,e,r){return i[e]=r,!0},has(i,e){return i instanceof IDBTransaction&&(e==="done"||e==="store")?!0:e in i}};function uv(i){ku=i(ku)}function cv(i){return i===IDBDatabase.prototype.transaction&&!("objectStoreNames"in IDBTransaction.prototype)?function(e,...r){const o=i.call(uu(this),e,...r);return vp.set(o,e.sort?e.sort():[e]),jr(o)}:ov().includes(i)?function(...e){return i.apply(uu(this),e),jr(gp.get(this))}:function(...e){return jr(i.apply(uu(this),e))}}function dv(i){return typeof i=="function"?cv(i):(i instanceof IDBTransaction&&lv(i),iv(i,sv())?new Proxy(i,ku):i)}function jr(i){if(i instanceof IDBRequest)return av(i);if(lu.has(i))return lu.get(i);const e=dv(i);return e!==i&&(lu.set(i,e),Ou.set(e,i)),e}const uu=i=>Ou.get(i);function hv(i,e,{blocked:r,upgrade:o,blocking:l,terminated:c}={}){const h=indexedDB.open(i,e),m=jr(h);return o&&h.addEventListener("upgradeneeded",f=>{o(jr(h.result),f.oldVersion,f.newVersion,jr(h.transaction),f)}),r&&h.addEventListener("blocked",f=>r(f.oldVersion,f.newVersion,f)),m.then(f=>{c&&f.addEventListener("close",()=>c()),l&&f.addEventListener("versionchange",v=>l(v.oldVersion,v.newVersion,v))}).catch(()=>{}),m}const fv=["get","getKey","getAll","getAllKeys","count"],pv=["put","add","delete","clear"],cu=new Map;function zh(i,e){if(!(i instanceof IDBDatabase&&!(e in i)&&typeof e=="string"))return;if(cu.get(e))return cu.get(e);const r=e.replace(/FromIndex$/,""),o=e!==r,l=pv.includes(r);if(!(r in(o?IDBIndex:IDBObjectStore).prototype)||!(l||fv.includes(r)))return;const c=async function(h,...m){const f=this.transaction(h,l?"readwrite":"readonly");let v=f.store;return o&&(v=v.index(m.shift())),(await Promise.all([v[r](...m),l&&f.done]))[0]};return cu.set(e,c),c}uv(i=>({...i,get:(e,r,o)=>zh(e,r)||i.get(e,r,o),has:(e,r)=>!!zh(e,r)||i.has(e,r)}));/**
 * @license
 * Copyright 2019 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */class mv{constructor(e){this.container=e}getPlatformInfoString(){return this.container.getProviders().map(r=>{if(gv(r)){const o=r.getImmediate();return`${o.library}/${o.version}`}else return null}).filter(r=>r).join(" ")}}function gv(i){const e=i.getComponent();return(e==null?void 0:e.type)==="VERSION"}const Tu="@firebase/app",jh="0.16.4";/**
 * @license
 * Copyright 2019 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */const lr=new mp("@firebase/app"),vv="@firebase/app-compat",yv="@firebase/analytics-compat",wv="@firebase/analytics",xv="@firebase/app-check-compat",_v="@firebase/app-check",Ev="@firebase/auth",Sv="@firebase/auth-compat",kv="@firebase/database",Tv="@firebase/data-connect",Cv="@firebase/database-compat",Iv="@firebase/functions",Rv="@firebase/functions-compat",Nv="@firebase/installations",Pv="@firebase/installations-compat",Av="@firebase/messaging",Mv="@firebase/messaging-compat",Dv="@firebase/performance",bv="@firebase/performance-compat",Lv="@firebase/remote-config",Ov="@firebase/remote-config-compat",Fv="@firebase/storage",zv="@firebase/storage-compat",jv="@firebase/firestore",Uv="@firebase/ai",Bv="@firebase/firestore-compat",$v="firebase",Vv="13.1.0";/**
 * @license
 * Copyright 2019 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */const Cu="[DEFAULT]",Hv={[Tu]:"fire-core",[vv]:"fire-core-compat",[wv]:"fire-analytics",[yv]:"fire-analytics-compat",[_v]:"fire-app-check",[xv]:"fire-app-check-compat",[Ev]:"fire-auth",[Sv]:"fire-auth-compat",[kv]:"fire-rtdb",[Tv]:"fire-data-connect",[Cv]:"fire-rtdb-compat",[Iv]:"fire-fn",[Rv]:"fire-fn-compat",[Nv]:"fire-iid",[Pv]:"fire-iid-compat",[Av]:"fire-fcm",[Mv]:"fire-fcm-compat",[Dv]:"fire-perf",[bv]:"fire-perf-compat",[Lv]:"fire-rc",[Ov]:"fire-rc-compat",[Fv]:"fire-gcs",[zv]:"fire-gcs-compat",[jv]:"fire-fst",[Bv]:"fire-fst-compat",[Uv]:"fire-vertex","fire-js":"fire-js",[$v]:"fire-js-all"};/**
 * @license
 * Copyright 2019 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */const Ms=new Map,Wv=new Map,Iu=new Map;function Uh(i,e){try{i.container.addComponent(e)}catch(r){lr.debug(`Component ${e.name} failed to register with FirebaseApp ${i.name}`,r)}}function Ds(i){const e=i.name;if(Iu.has(e))return lr.debug(`There were multiple attempts to register component ${e}.`),!1;Iu.set(e,i);for(const r of Ms.values())Uh(r,i);for(const r of Wv.values())Uh(r,i);return!0}function yp(i,e){const r=i.container.getProvider("heartbeat").getImmediate({optional:!0});return r&&r.triggerHeartbeat(),i.container.getProvider(e)}function rn(i){return i==null?!1:i.settings!==void 0}/**
 * @license
 * Copyright 2019 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */const Gv={"no-app":"No Firebase App '{$appName}' has been created - call initializeApp() first","bad-app-name":"Illegal App name: '{$appName}'","duplicate-app":"Firebase App named '{$appName}' already exists with different {$mismatchedParam}. Existing: '{$oldValue}'. New: '{$newValue}'.","app-deleted":"Firebase App named '{$appName}' already deleted","server-app-deleted":"Firebase Server App has been deleted","no-options":"Need to provide options, when not being deployed to hosting via source.","invalid-app-argument":"firebase.{$appName}() takes either no argument or a Firebase App instance.","invalid-log-argument":"First argument to `onLog` must be null or a function.","idb-open":"Error thrown when opening IndexedDB. Original error: {$originalErrorMessage}.","idb-get":"Error thrown when reading from IndexedDB. Original error: {$originalErrorMessage}.","idb-set":"Error thrown when writing to IndexedDB. Original error: {$originalErrorMessage}.","idb-delete":"Error thrown when deleting from IndexedDB. Original error: {$originalErrorMessage}.","finalization-registry-not-supported":"FirebaseServerApp deleteOnDeref field defined but the JS runtime does not support FinalizationRegistry.","invalid-server-app-environment":"FirebaseServerApp is not for use in browser environments."},sr=new Fs("app","Firebase",Gv);/**
 * @license
 * Copyright 2019 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */class qv{constructor(e,r,o){this._isDeleted=!1,this._options={...e},this._config={...r},this._name=r.name,this._automaticDataCollectionEnabled=r.automaticDataCollectionEnabled,this._container=o,this.container.addComponent(new Vi("app",()=>this,"PUBLIC"))}get automaticDataCollectionEnabled(){return this.checkDestroyed(),this._automaticDataCollectionEnabled}set automaticDataCollectionEnabled(e){this.checkDestroyed(),this._automaticDataCollectionEnabled=e}get name(){return this.checkDestroyed(),this._name}get options(){return this.checkDestroyed(),this._options}get config(){return this.checkDestroyed(),this._config}get container(){return this._container}get isDeleted(){return this._isDeleted}set isDeleted(e){this._isDeleted=e}checkDestroyed(){if(this.isDeleted)throw sr.create("app-deleted",{appName:this._name})}}/**
 * @license
 * Copyright 2019 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */const js=Vv;function wp(i,e={}){let r=i;typeof e!="object"&&(e={name:e});const o={name:Cu,automaticDataCollectionEnabled:!0,...e},l=o.name;if(typeof l!="string"||!l)throw sr.create("bad-app-name",{appName:String(l)});if(r||(r=hp()),!r)throw sr.create("no-options");const c=Ms.get(l);if(c)if($i(r,c.options)){if($i(o,c.config))return c;throw sr.create("duplicate-app",{appName:l,mismatchedParam:"config",oldValue:JSON.stringify(c.config),newValue:JSON.stringify(o)})}else throw sr.create("duplicate-app",{appName:l,mismatchedParam:"options",oldValue:JSON.stringify(c.options),newValue:JSON.stringify(r)});const h=new Z0(l);for(const f of Iu.values())h.addComponent(f);const m=new qv(r,o,h);return Ms.set(l,m),m}function xp(i=Cu){const e=Ms.get(i);if(!e&&i===Cu&&hp())return wp();if(!e)throw sr.create("no-app",{appName:i});return e}function Kv(){return Array.from(Ms.values())}function ji(i,e,r){let o=Hv[i]??i;r&&(o+=`-${r}`);const l=o.match(/\s|\//),c=e.match(/\s|\//);if(l||c){const h=[`Unable to register library "${o}" with version "${e}":`];l&&h.push(`library name "${o}" contains illegal characters (whitespace or "/")`),l&&c&&h.push("and"),c&&h.push(`version name "${e}" contains illegal characters (whitespace or "/")`),lr.warn(h.join(" "));return}Ds(new Vi(`${o}-version`,()=>({library:o,version:e}),"VERSION"))}/**
 * @license
 * Copyright 2021 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */const Xv="firebase-heartbeat-database",Yv=1,bs="firebase-heartbeat-store";let du=null;function _p(){return du||(du=hv(Xv,Yv,{upgrade:(i,e)=>{switch(e){case 0:try{i.createObjectStore(bs)}catch(r){console.warn(r)}}}}).catch(i=>{throw sr.create("idb-open",{originalErrorMessage:i.message})})),du}async function Qv(i){try{const r=(await _p()).transaction(bs),o=await r.objectStore(bs).get(Ep(i));return await r.done,o}catch(e){if(e instanceof Br)lr.warn(e.message);else{const r=sr.create("idb-get",{originalErrorMessage:e==null?void 0:e.message});lr.warn(r.message)}}}async function Bh(i,e){try{const o=(await _p()).transaction(bs,"readwrite");await o.objectStore(bs).put(e,Ep(i)),await o.done}catch(r){if(r instanceof Br)lr.warn(r.message);else{const o=sr.create("idb-set",{originalErrorMessage:r==null?void 0:r.message});lr.warn(o.message)}}}function Ep(i){return`${i.name}!${i.options.appId}`}/**
 * @license
 * Copyright 2021 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */const Jv=1024,Zv=30;class e1{constructor(e){this.container=e,this._heartbeatsCache=null;const r=this.container.getProvider("app").getImmediate();this._storage=new n1(r),this._heartbeatsCachePromise=this._storage.read().then(o=>(this._heartbeatsCache=o,o))}async triggerHeartbeat(){var e,r;try{const l=this.container.getProvider("platform-logger").getImmediate().getPlatformInfoString(),c=$h();if(((e=this._heartbeatsCache)==null?void 0:e.heartbeats)==null&&(this._heartbeatsCache=await this._heartbeatsCachePromise,((r=this._heartbeatsCache)==null?void 0:r.heartbeats)==null)||this._heartbeatsCache.lastSentHeartbeatDate===c||this._heartbeatsCache.heartbeats.some(h=>h.date===c))return;if(this._heartbeatsCache.heartbeats.push({date:c,agent:l}),this._heartbeatsCache.heartbeats.length>Zv){const h=r1(this._heartbeatsCache.heartbeats);this._heartbeatsCache.heartbeats.splice(h,1)}return this._storage.overwrite(this._heartbeatsCache)}catch(o){lr.warn(o)}}async getHeartbeatsHeader(){var e;try{if(this._heartbeatsCache===null&&await this._heartbeatsCachePromise,((e=this._heartbeatsCache)==null?void 0:e.heartbeats)==null||this._heartbeatsCache.heartbeats.length===0)return"";const r=$h(),{heartbeatsToSend:o,unsentEntries:l}=t1(this._heartbeatsCache.heartbeats),c=cp(JSON.stringify({version:2,heartbeats:o}));return this._heartbeatsCache.lastSentHeartbeatDate=r,l.length>0?(this._heartbeatsCache.heartbeats=l,await this._storage.overwrite(this._heartbeatsCache)):(this._heartbeatsCache.heartbeats=[],this._storage.overwrite(this._heartbeatsCache)),c}catch(r){return lr.warn(r),""}}}function $h(){return new Date().toISOString().substring(0,10)}function t1(i,e=Jv){const r=[];let o=i.slice();for(const l of i){const c=r.find(h=>h.agent===l.agent);if(c){if(c.dates.push(l.date),Vh(r)>e){c.dates.pop();break}}else if(r.push({agent:l.agent,dates:[l.date]}),Vh(r)>e){r.pop();break}o=o.slice(1)}return{heartbeatsToSend:r,unsentEntries:o}}class n1{constructor(e){this.app=e,this._canUseIndexedDBPromise=this.runIndexedDBEnvironmentCheck()}async runIndexedDBEnvironmentCheck(){return B0()?$0().then(()=>!0).catch(()=>!1):!1}async read(){if(await this._canUseIndexedDBPromise){const r=await Qv(this.app);return r!=null&&r.heartbeats?r:{heartbeats:[]}}else return{heartbeats:[]}}async overwrite(e){if(await this._canUseIndexedDBPromise){const o=await this.read();return Bh(this.app,{lastSentHeartbeatDate:e.lastSentHeartbeatDate??o.lastSentHeartbeatDate,heartbeats:e.heartbeats})}else return}async add(e){if(await this._canUseIndexedDBPromise){const o=await this.read();return Bh(this.app,{lastSentHeartbeatDate:e.lastSentHeartbeatDate??o.lastSentHeartbeatDate,heartbeats:[...o.heartbeats,...e.heartbeats]})}else return}}function Vh(i){return cp(JSON.stringify({version:2,heartbeats:i})).length}function r1(i){if(i.length===0)return-1;let e=0,r=i[0].date;for(let o=1;o<i.length;o++)i[o].date<r&&(r=i[o].date,e=o);return e}/**
 * @license
 * Copyright 2019 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */function i1(i){Ds(new Vi("platform-logger",e=>new mv(e),"PRIVATE")),Ds(new Vi("heartbeat",e=>new e1(e),"PRIVATE")),ji(Tu,jh,i),ji(Tu,jh,"esm2020"),ji("fire-js","")}/**
 * @license
 * Copyright 2019 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */i1("");var s1="firebase",o1="13.1.0";/**
 * @license
 * Copyright 2020 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */ji(s1,o1,"app");function Sp(){return{"dependent-sdk-initialized-before-auth":"Another Firebase SDK was initialized and is trying to use Auth before Auth is initialized. Please be sure to call `initializeAuth` or `getAuth` before starting any other Firebase SDK."}}const a1=Sp,kp=new Fs("auth","Firebase",Sp());/**
 * @license
 * Copyright 2020 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */const aa=new mp("@firebase/auth");function na(i,...e){aa.logLevel<=We.WARN&&aa.warn(`Auth (${js}): ${i}`,...e)}function ra(i,...e){aa.logLevel<=We.ERROR&&aa.error(`Auth (${js}): ${i}`,...e)}/**
 * @license
 * Copyright 2020 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */function vn(i,...e){throw Fu(i,...e)}function Pn(i,...e){return Fu(i,...e)}function ga(i,e,r){const o={...a1(),[e]:r};return new Fs("auth","Firebase",o).create(e,{appName:i.name})}function jn(i){return ga(i,"operation-not-supported-in-this-environment","Operations that alter the current user are not supported in conjunction with FirebaseServerApp")}function Tp(i,e,r){const o=r;if(!(e instanceof o))throw o.name!==e.constructor.name&&vn(i,"argument-error"),ga(i,"argument-error",`Type of ${e.constructor.name} does not match expected instance.Did you pass a reference from a different Auth SDK?`)}function Fu(i,...e){if(typeof i!="string"){const r=e[0],o=[...e.slice(1)];return o[0]&&(o[0].appName=i.name),i._errorFactory.create(r,...o)}return kp.create(i,...e)}function Ee(i,e,...r){if(!i)throw Fu(e,...r)}function or(i){const e="INTERNAL ASSERTION FAILED: "+i;throw ra(e),new Error(e)}function ur(i,e){i||or(e)}/**
 * @license
 * Copyright 2020 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */function Ru(){var i;return typeof self<"u"&&((i=self.location)==null?void 0:i.href)||""}function l1(){return Hh()==="http:"||Hh()==="https:"}function Hh(){var i;return typeof self<"u"&&((i=self.location)==null?void 0:i.protocol)||null}/**
 * @license
 * Copyright 2020 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */function u1(){return typeof navigator<"u"&&navigator&&"onLine"in navigator&&typeof navigator.onLine=="boolean"&&(l1()||z0()||"connection"in navigator)?navigator.onLine:!0}function c1(){if(typeof navigator>"u")return null;const i=navigator;return i.languages&&i.languages[0]||i.language||null}/**
 * @license
 * Copyright 2020 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */class Us{constructor(e,r){this.shortDelay=e,this.longDelay=r,ur(r>e,"Short delay should be less than long delay!"),this.isMobile=O0()||j0()}get(){return u1()?this.isMobile?this.longDelay:this.shortDelay:Math.min(5e3,this.shortDelay)}}/**
 * @license
 * Copyright 2020 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */function zu(i,e){ur(i.emulator,"Emulator should always be set here");const{url:r}=i.emulator;return e?`${r}${e.startsWith("/")?e.slice(1):e}`:r}/**
 * @license
 * Copyright 2020 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */class Cp{static initialize(e,r,o){this.fetchImpl=e,r&&(this.headersImpl=r),o&&(this.responseImpl=o)}static fetch(){if(this.fetchImpl)return this.fetchImpl;if(typeof self<"u"&&"fetch"in self)return self.fetch;if(typeof globalThis<"u"&&globalThis.fetch)return globalThis.fetch;if(typeof fetch<"u")return fetch;or("Could not find fetch implementation, make sure you call FetchProvider.initialize() with an appropriate polyfill")}static headers(){if(this.headersImpl)return this.headersImpl;if(typeof self<"u"&&"Headers"in self)return self.Headers;if(typeof globalThis<"u"&&globalThis.Headers)return globalThis.Headers;if(typeof Headers<"u")return Headers;or("Could not find Headers implementation, make sure you call FetchProvider.initialize() with an appropriate polyfill")}static response(){if(this.responseImpl)return this.responseImpl;if(typeof self<"u"&&"Response"in self)return self.Response;if(typeof globalThis<"u"&&globalThis.Response)return globalThis.Response;if(typeof Response<"u")return Response;or("Could not find Response implementation, make sure you call FetchProvider.initialize() with an appropriate polyfill")}}/**
 * @license
 * Copyright 2020 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */const d1={CREDENTIAL_MISMATCH:"custom-token-mismatch",MISSING_CUSTOM_TOKEN:"internal-error",INVALID_IDENTIFIER:"invalid-email",MISSING_CONTINUE_URI:"internal-error",INVALID_PASSWORD:"wrong-password",MISSING_PASSWORD:"missing-password",INVALID_LOGIN_CREDENTIALS:"invalid-credential",EMAIL_EXISTS:"email-already-in-use",PASSWORD_LOGIN_DISABLED:"operation-not-allowed",INVALID_IDP_RESPONSE:"invalid-credential",INVALID_PENDING_TOKEN:"invalid-credential",FEDERATED_USER_ID_ALREADY_LINKED:"credential-already-in-use",MISSING_REQ_TYPE:"internal-error",EMAIL_NOT_FOUND:"user-not-found",RESET_PASSWORD_EXCEED_LIMIT:"too-many-requests",EXPIRED_OOB_CODE:"expired-action-code",INVALID_OOB_CODE:"invalid-action-code",MISSING_OOB_CODE:"internal-error",CREDENTIAL_TOO_OLD_LOGIN_AGAIN:"requires-recent-login",INVALID_ID_TOKEN:"invalid-user-token",TOKEN_EXPIRED:"user-token-expired",USER_NOT_FOUND:"user-token-expired",TOO_MANY_ATTEMPTS_TRY_LATER:"too-many-requests",PASSWORD_DOES_NOT_MEET_REQUIREMENTS:"password-does-not-meet-requirements",INVALID_CODE:"invalid-verification-code",INVALID_SESSION_INFO:"invalid-verification-id",INVALID_TEMPORARY_PROOF:"invalid-credential",MISSING_SESSION_INFO:"missing-verification-id",SESSION_EXPIRED:"code-expired",MISSING_ANDROID_PACKAGE_NAME:"missing-android-pkg-name",UNAUTHORIZED_DOMAIN:"unauthorized-continue-uri",INVALID_OAUTH_CLIENT_ID:"invalid-oauth-client-id",ADMIN_ONLY_OPERATION:"admin-restricted-operation",INVALID_MFA_PENDING_CREDENTIAL:"invalid-multi-factor-session",MFA_ENROLLMENT_NOT_FOUND:"multi-factor-info-not-found",MISSING_MFA_ENROLLMENT_ID:"missing-multi-factor-info",MISSING_MFA_PENDING_CREDENTIAL:"missing-multi-factor-session",SECOND_FACTOR_EXISTS:"second-factor-already-in-use",SECOND_FACTOR_LIMIT_EXCEEDED:"maximum-second-factor-count-exceeded",BLOCKING_FUNCTION_ERROR_RESPONSE:"internal-error",RECAPTCHA_NOT_ENABLED:"recaptcha-not-enabled",MISSING_RECAPTCHA_TOKEN:"missing-recaptcha-token",INVALID_RECAPTCHA_TOKEN:"invalid-recaptcha-token",INVALID_RECAPTCHA_ACTION:"invalid-recaptcha-action",MISSING_CLIENT_TYPE:"missing-client-type",MISSING_RECAPTCHA_VERSION:"missing-recaptcha-version",INVALID_RECAPTCHA_VERSION:"invalid-recaptcha-version",INVALID_REQ_TYPE:"invalid-req-type"};/**
 * @license
 * Copyright 2020 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */const h1=["/v1/accounts:signInWithCustomToken","/v1/accounts:signInWithEmailLink","/v1/accounts:signInWithIdp","/v1/accounts:signInWithPassword","/v1/accounts:signInWithPhoneNumber","/v1/token"],f1=new Us(3e4,6e4);function cr(i,e){return i.tenantId&&!e.tenantId?{...e,tenantId:i.tenantId}:e}async function $n(i,e,r,o,l={}){return Ip(i,l,async()=>{let c={},h={};o&&(e==="GET"?h=o:c={body:JSON.stringify(o)});const m=zs({...h,key:i.config.apiKey}).slice(1),f=await i._getAdditionalHeaders();f["Content-Type"]="application/json",i.languageCode&&(f["X-Firebase-Locale"]=i.languageCode);const v={method:e,headers:f,...c};return F0()||(v.referrerPolicy="strict-origin-when-cross-origin"),i.emulatorConfig&&Lu(i.emulatorConfig.host)&&(v.credentials="include"),Cp.fetch()(await Rp(i,i.config.apiHost,r,m),v)})}async function Ip(i,e,r){i._canInitEmulator=!1;const o={...d1,...e};try{const l=new m1(i),c=await Promise.race([r(),l.promise]);l.clearNetworkTimeout();const h=await c.json();if("needConfirmation"in h)throw Qo(i,"account-exists-with-different-credential",h);if(c.ok&&!("errorMessage"in h))return h;{const m=c.ok?h.errorMessage:h.error.message,[f,v]=m.split(" : ");if(f==="FEDERATED_USER_ID_ALREADY_LINKED")throw Qo(i,"credential-already-in-use",h);if(f==="EMAIL_EXISTS")throw Qo(i,"email-already-in-use",h);if(f==="USER_DISABLED")throw Qo(i,"user-disabled",h);const x=o[f]||f.toLowerCase().replace(/[_\s]+/g,"-");if(v)throw ga(i,x,v);vn(i,x)}}catch(l){if(l instanceof Br)throw l;vn(i,"network-request-failed",{message:String(l)})}}async function Bs(i,e,r,o,l={}){const c=await $n(i,e,r,o,l);return"mfaPendingCredential"in c&&vn(i,"multi-factor-auth-required",{_serverResponse:c}),c}async function Rp(i,e,r,o){const l=`${e}${r}?${o}`,c=i,h=c.config.emulator?zu(i.config,l):`${i.config.apiScheme}://${l}`;return h1.includes(r)&&(await c._persistenceManagerAvailable,c._getPersistenceType()==="COOKIE")?c._getPersistence()._getFinalTarget(h).toString():h}function p1(i){switch(i){case"ENFORCE":return"ENFORCE";case"AUDIT":return"AUDIT";case"OFF":return"OFF";default:return"ENFORCEMENT_STATE_UNSPECIFIED"}}class m1{clearNetworkTimeout(){clearTimeout(this.timer)}constructor(e){this.auth=e,this.timer=null,this.promise=new Promise((r,o)=>{this.timer=setTimeout(()=>o(Pn(this.auth,"network-request-failed")),f1.get())})}}function Qo(i,e,r){const o={appName:i.name};r.email&&(o.email=r.email),r.phoneNumber&&(o.phoneNumber=r.phoneNumber);const l=Pn(i,e,o);return l.customData._tokenResponse=r,l}function Wh(i){return i!==void 0&&i.enterprise!==void 0}class g1{constructor(e){if(this.siteKey="",this.recaptchaEnforcementState=[],e.recaptchaKey===void 0)throw new Error("recaptchaKey undefined");this.siteKey=e.recaptchaKey.split("/")[3],this.recaptchaEnforcementState=e.recaptchaEnforcementState}getProviderEnforcementState(e){if(!this.recaptchaEnforcementState||this.recaptchaEnforcementState.length===0)return null;for(const r of this.recaptchaEnforcementState)if(r.provider&&r.provider===e)return p1(r.enforcementState);return null}isProviderEnabled(e){return this.getProviderEnforcementState(e)==="ENFORCE"||this.getProviderEnforcementState(e)==="AUDIT"}isAnyProviderEnabled(){return this.isProviderEnabled("EMAIL_PASSWORD_PROVIDER")||this.isProviderEnabled("PHONE_PROVIDER")}}async function v1(i,e){return $n(i,"GET","/v2/recaptchaConfig",cr(i,e))}/**
 * @license
 * Copyright 2020 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */async function y1(i,e){return $n(i,"POST","/v1/accounts:delete",e)}async function la(i,e){return $n(i,"POST","/v1/accounts:lookup",e)}/**
 * @license
 * Copyright 2020 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */function Ps(i){if(i)try{const e=new Date(Number(i));if(!isNaN(e.getTime()))return e.toUTCString()}catch{}}async function w1(i,e=!1){const r=Bn(i),o=await r.getIdToken(e),l=ju(o);Ee(l&&l.exp&&l.auth_time&&l.iat,r.auth,"internal-error");const c=typeof l.firebase=="object"?l.firebase:void 0,h=c==null?void 0:c.sign_in_provider;return{claims:l,token:o,authTime:Ps(hu(l.auth_time)),issuedAtTime:Ps(hu(l.iat)),expirationTime:Ps(hu(l.exp)),signInProvider:h||null,signInSecondFactor:(c==null?void 0:c.sign_in_second_factor)||null}}function hu(i){return Number(i)*1e3}function ju(i){const[e,r,o]=i.split(".");if(e===void 0||r===void 0||o===void 0)return ra("JWT malformed, contained fewer than 3 sections"),null;try{const l=dp(r);return l?JSON.parse(l):(ra("Failed to decode base64 JWT payload"),null)}catch(l){return ra("Caught error parsing JWT payload as JSON",l==null?void 0:l.toString()),null}}function Gh(i){const e=ju(i);return Ee(e,"internal-error"),Ee(typeof e.exp<"u","internal-error"),Ee(typeof e.iat<"u","internal-error"),Number(e.exp)-Number(e.iat)}/**
 * @license
 * Copyright 2020 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */async function Hi(i,e,r=!1){if(r)return e;try{return await e}catch(o){throw Np(o)&&i.auth.currentUser===i&&await i.auth.signOut(),o}}function Np(i){return i instanceof Br?i.code==="auth/user-disabled"||i.code==="auth/user-token-expired":!1}/**
 * @license
 * Copyright 2020 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */class x1{constructor(e){this.user=e,this.isRunning=!1,this.timerId=null,this.errorBackoff=3e4}_start(){this.isRunning||(this.isRunning=!0,this.schedule())}_stop(){this.isRunning&&(this.isRunning=!1,this.timerId!==null&&clearTimeout(this.timerId))}getInterval(e){if(e){const r=this.errorBackoff;return this.errorBackoff=Math.min(this.errorBackoff*2,96e4),r}else{this.errorBackoff=3e4;const o=(this.user.stsTokenManager.expirationTime??0)-Date.now()-3e5;return Math.max(0,o)}}schedule(e=!1){if(!this.isRunning)return;const r=this.getInterval(e);this.timerId=setTimeout(async()=>{await this.iteration()},r)}async iteration(){try{await this.user.getIdToken(!0)}catch(e){(e==null?void 0:e.code)==="auth/network-request-failed"&&this.schedule(!0);return}this.schedule()}}/**
 * @license
 * Copyright 2020 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */class Nu{constructor(e,r){this.createdAt=e,this.lastLoginAt=r,this._initializeTime()}_initializeTime(){this.lastSignInTime=Ps(this.lastLoginAt),this.creationTime=Ps(this.createdAt)}_copy(e){this.createdAt=e.createdAt,this.lastLoginAt=e.lastLoginAt,this._initializeTime()}toJSON(){return{createdAt:this.createdAt,lastLoginAt:this.lastLoginAt}}}/**
 * @license
 * Copyright 2019 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */async function ua(i){var S;const e=i.auth,r=await i.getIdToken(),o=await Hi(i,la(e,{idToken:r}));Ee(o==null?void 0:o.users.length,e,"internal-error");const l=o.users[0];i._notifyReloadListener(l);const c=(S=l.providerUserInfo)!=null&&S.length?Pp(l.providerUserInfo):[],h=E1(i.providerData,c),m=i.isAnonymous,f=!(i.email&&l.passwordHash)&&!(h!=null&&h.length),v=m?f:!1,x={uid:l.localId,displayName:l.displayName||null,photoURL:l.photoUrl||null,email:l.email||null,emailVerified:l.emailVerified||!1,phoneNumber:l.phoneNumber||null,tenantId:l.tenantId||null,providerData:h,metadata:new Nu(l.createdAt,l.lastLoginAt),isAnonymous:v};Object.assign(i,x)}async function _1(i){const e=Bn(i);await ua(e),await e.auth._persistUserIfCurrent(e),e.auth._notifyListenersIfCurrent(e)}function E1(i,e){return[...i.filter(o=>!e.some(l=>l.providerId===o.providerId)),...e]}function Pp(i){return i.map(({providerId:e,...r})=>({providerId:e,uid:r.rawId||"",displayName:r.displayName||null,email:r.email||null,phoneNumber:r.phoneNumber||null,photoURL:r.photoUrl||null}))}/**
 * @license
 * Copyright 2020 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */async function S1(i,e){const r=await Ip(i,{},async()=>{const o=zs({grant_type:"refresh_token",refresh_token:e}).slice(1),{tokenApiHost:l,apiKey:c}=i.config,h=await Rp(i,l,"/v1/token",`key=${c}`),m=await i._getAdditionalHeaders();m["Content-Type"]="application/x-www-form-urlencoded";const f={method:"POST",headers:m,body:o};return i.emulatorConfig&&Lu(i.emulatorConfig.host)&&(f.credentials="include"),Cp.fetch()(h,f)});return{accessToken:r.access_token,expiresIn:r.expires_in,refreshToken:r.refresh_token}}async function k1(i,e){return $n(i,"POST","/v2/accounts:revokeToken",cr(i,e))}/**
 * @license
 * Copyright 2020 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */class Ui{constructor(){this.refreshToken=null,this.accessToken=null,this.expirationTime=null}get isExpired(){return!this.expirationTime||Date.now()>this.expirationTime-3e4}updateFromServerResponse(e){Ee(e.idToken,"internal-error"),Ee(typeof e.idToken<"u","internal-error"),Ee(typeof e.refreshToken<"u","internal-error");const r="expiresIn"in e&&typeof e.expiresIn<"u"?Number(e.expiresIn):Gh(e.idToken);this.updateTokensAndExpiration(e.idToken,e.refreshToken,r)}updateFromIdToken(e){Ee(e.length!==0,"internal-error");const r=Gh(e);this.updateTokensAndExpiration(e,null,r)}async getToken(e,r=!1){return!r&&this.accessToken&&!this.isExpired?this.accessToken:(Ee(this.refreshToken,e,"user-token-expired"),this.refreshToken?(await this.refresh(e,this.refreshToken),this.accessToken):null)}clearRefreshToken(){this.refreshToken=null}async refresh(e,r){const{accessToken:o,refreshToken:l,expiresIn:c}=await S1(e,r);this.updateTokensAndExpiration(o,l,Number(c))}updateTokensAndExpiration(e,r,o){this.refreshToken=r||null,this.accessToken=e||null,this.expirationTime=Date.now()+o*1e3}static fromJSON(e,r){const{refreshToken:o,accessToken:l,expirationTime:c}=r,h=new Ui;return o&&(Ee(typeof o=="string","internal-error",{appName:e}),h.refreshToken=o),l&&(Ee(typeof l=="string","internal-error",{appName:e}),h.accessToken=l),c&&(Ee(typeof c=="number","internal-error",{appName:e}),h.expirationTime=c),h}toJSON(){return{refreshToken:this.refreshToken,accessToken:this.accessToken,expirationTime:this.expirationTime}}_assign(e){this.accessToken=e.accessToken,this.refreshToken=e.refreshToken,this.expirationTime=e.expirationTime}_clone(){return Object.assign(new Ui,this.toJSON())}_performRefresh(){return or("not implemented")}}/**
 * @license
 * Copyright 2020 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */function br(i,e){Ee(typeof i=="string"||typeof i>"u","internal-error",{appName:e})}class Rn{constructor({uid:e,auth:r,stsTokenManager:o,...l}){this.providerId="firebase",this.proactiveRefresh=new x1(this),this.reloadUserInfo=null,this.reloadListener=null,this.uid=e,this.auth=r,this.stsTokenManager=o,this.accessToken=o.accessToken,this.displayName=l.displayName||null,this.email=l.email||null,this.emailVerified=l.emailVerified||!1,this.phoneNumber=l.phoneNumber||null,this.photoURL=l.photoURL||null,this.isAnonymous=l.isAnonymous||!1,this.tenantId=l.tenantId||null,this.providerData=l.providerData?[...l.providerData]:[],this.metadata=new Nu(l.createdAt||void 0,l.lastLoginAt||void 0)}async getIdToken(e){const r=await Hi(this,this.stsTokenManager.getToken(this.auth,e));return Ee(r,this.auth,"internal-error"),this.accessToken!==r&&(this.accessToken=r,await this.auth._persistUserIfCurrent(this),this.auth._notifyListenersIfCurrent(this)),r}getIdTokenResult(e){return w1(this,e)}reload(){return _1(this)}_assign(e){this!==e&&(Ee(this.uid===e.uid,this.auth,"internal-error"),this.displayName=e.displayName,this.photoURL=e.photoURL,this.email=e.email,this.emailVerified=e.emailVerified,this.phoneNumber=e.phoneNumber,this.isAnonymous=e.isAnonymous,this.tenantId=e.tenantId,this.providerData=e.providerData.map(r=>({...r})),this.metadata._copy(e.metadata),this.stsTokenManager._assign(e.stsTokenManager))}_clone(e){const r=new Rn({...this,auth:e,stsTokenManager:this.stsTokenManager._clone()});return r.metadata._copy(this.metadata),r}_onReload(e){Ee(!this.reloadListener,this.auth,"internal-error"),this.reloadListener=e,this.reloadUserInfo&&(this._notifyReloadListener(this.reloadUserInfo),this.reloadUserInfo=null)}_notifyReloadListener(e){this.reloadListener?this.reloadListener(e):this.reloadUserInfo=e}_startProactiveRefresh(){this.proactiveRefresh._start()}_stopProactiveRefresh(){this.proactiveRefresh._stop()}async _updateTokensIfNecessary(e,r=!1){let o=!1;e.idToken&&e.idToken!==this.stsTokenManager.accessToken&&(this.stsTokenManager.updateFromServerResponse(e),o=!0),r&&await ua(this),await this.auth._persistUserIfCurrent(this),o&&this.auth._notifyListenersIfCurrent(this)}async delete(){if(rn(this.auth.app))return Promise.reject(jn(this.auth));const e=await this.getIdToken();return await Hi(this,y1(this.auth,{idToken:e})),this.stsTokenManager.clearRefreshToken(),this.auth.signOut()}toJSON(){return{uid:this.uid,email:this.email||void 0,emailVerified:this.emailVerified,displayName:this.displayName||void 0,isAnonymous:this.isAnonymous,photoURL:this.photoURL||void 0,phoneNumber:this.phoneNumber||void 0,tenantId:this.tenantId||void 0,providerData:this.providerData.map(e=>({...e})),stsTokenManager:this.stsTokenManager.toJSON(),_redirectEventId:this._redirectEventId,...this.metadata.toJSON(),apiKey:this.auth.config.apiKey,appName:this.auth.name}}get refreshToken(){return this.stsTokenManager.refreshToken||""}static _fromJSON(e,r){const o=r.displayName??void 0,l=r.email??void 0,c=r.phoneNumber??void 0,h=r.photoURL??void 0,m=r.tenantId??void 0,f=r._redirectEventId??void 0,v=r.createdAt??void 0,x=r.lastLoginAt??void 0,{uid:S,emailVerified:T,isAnonymous:R,providerData:P,stsTokenManager:b}=r;Ee(S&&b,e,"internal-error");const A=Ui.fromJSON(this.name,b);Ee(typeof S=="string",e,"internal-error"),br(o,e.name),br(l,e.name),Ee(typeof T=="boolean",e,"internal-error"),Ee(typeof R=="boolean",e,"internal-error"),br(c,e.name),br(h,e.name),br(m,e.name),br(f,e.name),br(v,e.name),br(x,e.name);const F=new Rn({uid:S,auth:e,email:l,emailVerified:T,displayName:o,isAnonymous:R,photoURL:h,phoneNumber:c,tenantId:m,stsTokenManager:A,createdAt:v,lastLoginAt:x});return P&&Array.isArray(P)&&(F.providerData=P.map(se=>({...se}))),f&&(F._redirectEventId=f),F}static async _fromIdTokenResponse(e,r,o=!1){const l=new Ui;l.updateFromServerResponse(r);const c=new Rn({uid:r.localId,auth:e,stsTokenManager:l,isAnonymous:o});return await ua(c),c}static async _fromGetAccountInfoResponse(e,r,o){const l=r.users[0];Ee(l.localId!==void 0,"internal-error");const c=l.providerUserInfo!==void 0?Pp(l.providerUserInfo):[],h=!(l.email&&l.passwordHash)&&!(c!=null&&c.length),m=new Ui;m.updateFromIdToken(o);const f=new Rn({uid:l.localId,auth:e,stsTokenManager:m,isAnonymous:h}),v={uid:l.localId,displayName:l.displayName||null,photoURL:l.photoUrl||null,email:l.email||null,emailVerified:l.emailVerified||!1,phoneNumber:l.phoneNumber||null,tenantId:l.tenantId||null,providerData:c,metadata:new Nu(l.createdAt,l.lastLoginAt),isAnonymous:!(l.email&&l.passwordHash)&&!(c!=null&&c.length)};return Object.assign(f,v),f}}/**
 * @license
 * Copyright 2020 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */const qh=new Map;function ar(i){ur(i instanceof Function,"Expected a class definition");let e=qh.get(i);return e?(ur(e instanceof i,"Instance stored in cache mismatched with class"),e):(e=new i,qh.set(i,e),e)}/**
 * @license
 * Copyright 2019 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */class Ap{constructor(){this.type="NONE",this.storage={}}async _isAvailable(){return!0}async _set(e,r){this.storage[e]=r}async _get(e){const r=this.storage[e];return r===void 0?null:r}async _remove(e){delete this.storage[e]}_addListener(e,r){}_removeListener(e,r){}}Ap.type="NONE";const Kh=Ap;/**
 * @license
 * Copyright 2019 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */function ia(i,e,r){return`firebase:${i}:${e}:${r}`}class li{constructor(e,r,o){this.persistence=e,this.auth=r,this.userKey=o;const{config:l,name:c}=this.auth;this.fullUserKey=ia(this.userKey,l.apiKey,c),this.fullPersistenceKey=ia("persistence",l.apiKey,c),this.boundEventHandler=r._onStorageEvent.bind(r);try{this.persistence._addListener(this.fullUserKey,this.boundEventHandler)}catch{}}setCurrentUser(e){return this.persistence._set(this.fullUserKey,e.toJSON())}async getCurrentUser(){const e=await this.persistence._get(this.fullUserKey);if(!e)return null;if(typeof e=="string"){const r=await la(this.auth,{idToken:e}).catch(()=>{});return r?Rn._fromGetAccountInfoResponse(this.auth,r,e):null}return Rn._fromJSON(this.auth,e)}removeCurrentUser(){return this.persistence._remove(this.fullUserKey)}savePersistenceForRedirect(){return this.persistence._set(this.fullPersistenceKey,this.persistence.type)}async setPersistence(e){if(this.persistence===e)return;const r=await this.getCurrentUser();if(await this.removeCurrentUser(),this.persistence=e,r)return this.setCurrentUser(r)}delete(){try{this.persistence._removeListener(this.fullUserKey,this.boundEventHandler)}catch{}}static async create(e,r,o="authUser"){if(!r.length)return new li(ar(Kh),e,o);const l=(await Promise.all(r.map(async v=>{try{if(await v._isAvailable())return v}catch{return}}))).filter(v=>v);let c=l[0]||ar(Kh);const h=ia(o,e.config.apiKey,e.name);let m=null;for(const v of r)try{const x=await v._get(h);if(x){let S;if(typeof x=="string"){const T=await la(e,{idToken:x}).catch(()=>{});if(!T)break;S=await Rn._fromGetAccountInfoResponse(e,T,x)}else S=Rn._fromJSON(e,x);v!==c&&(m=S),c=v;break}}catch{}const f=l.filter(v=>v._shouldAllowMigration);return!c._shouldAllowMigration||!f.length?new li(c,e,o):(c=f[0],m&&await c._set(h,m.toJSON()),await Promise.all(r.map(async v=>{if(v!==c)try{await v._remove(h)}catch{}})),new li(c,e,o))}}/**
 * @license
 * Copyright 2020 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */function Xh(i){const e=i.toLowerCase();if(e.includes("opera/")||e.includes("opr/")||e.includes("opios/"))return"Opera";if(Lp(e))return"IEMobile";if(e.includes("msie")||e.includes("trident/"))return"IE";if(e.includes("edge/"))return"Edge";if(Mp(e))return"Firefox";if(e.includes("silk/"))return"Silk";if(Fp(e))return"Blackberry";if(zp(e))return"Webos";if(Dp(e))return"Safari";if((e.includes("chrome/")||bp(e))&&!e.includes("edge/"))return"Chrome";if(Op(e))return"Android";{const r=/([a-zA-Z\d\.]+)\/[a-zA-Z\d\.]*$/,o=i.match(r);if((o==null?void 0:o.length)===2)return o[1]}return"Other"}function Mp(i=Lt()){return/firefox\//i.test(i)}function Dp(i=Lt()){const e=i.toLowerCase();return e.includes("safari/")&&!e.includes("chrome/")&&!e.includes("crios/")&&!e.includes("android")}function bp(i=Lt()){return/crios\//i.test(i)}function Lp(i=Lt()){return/iemobile/i.test(i)}function Op(i=Lt()){return/android/i.test(i)}function Fp(i=Lt()){return/blackberry/i.test(i)}function zp(i=Lt()){return/webos/i.test(i)}function Uu(i=Lt()){return/iphone|ipad|ipod/i.test(i)||/macintosh/i.test(i)&&/mobile/i.test(i)}function T1(i=Lt()){var e;return Uu(i)&&!!((e=window.navigator)!=null&&e.standalone)}function C1(){return U0()&&document.documentMode===10}function jp(i=Lt()){return Uu(i)||Op(i)||zp(i)||Fp(i)||/windows phone/i.test(i)||Lp(i)}/**
 * @license
 * Copyright 2020 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */function Up(i,e=[]){let r;switch(i){case"Browser":r=Xh(Lt());break;case"Worker":r=`${Xh(Lt())}-${i}`;break;default:r=i}const o=e.length?e.join(","):"FirebaseCore-web";return`${r}/JsCore/${js}/${o}`}/**
 * @license
 * Copyright 2022 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */class I1{constructor(e){this.auth=e,this.queue=[]}pushCallback(e,r){const o=c=>new Promise((h,m)=>{try{const f=e(c);h(f)}catch(f){m(f)}});o.onAbort=r,this.queue.push(o);const l=this.queue.length-1;return()=>{this.queue[l]=()=>Promise.resolve()}}async runMiddleware(e){if(this.auth.currentUser===e)return;const r=[];try{for(const o of this.queue)await o(e),o.onAbort&&r.push(o.onAbort)}catch(o){r.reverse();for(const l of r)try{l()}catch{}throw this.auth._errorFactory.create("login-blocked",{originalMessage:o==null?void 0:o.message})}}}/**
 * @license
 * Copyright 2023 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */async function R1(i,e={}){return $n(i,"GET","/v2/passwordPolicy",cr(i,e))}/**
 * @license
 * Copyright 2023 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */const N1=6;class P1{constructor(e){var o;const r=e.customStrengthOptions;this.customStrengthOptions={},this.customStrengthOptions.minPasswordLength=r.minPasswordLength??N1,r.maxPasswordLength&&(this.customStrengthOptions.maxPasswordLength=r.maxPasswordLength),r.containsLowercaseCharacter!==void 0&&(this.customStrengthOptions.containsLowercaseLetter=r.containsLowercaseCharacter),r.containsUppercaseCharacter!==void 0&&(this.customStrengthOptions.containsUppercaseLetter=r.containsUppercaseCharacter),r.containsNumericCharacter!==void 0&&(this.customStrengthOptions.containsNumericCharacter=r.containsNumericCharacter),r.containsNonAlphanumericCharacter!==void 0&&(this.customStrengthOptions.containsNonAlphanumericCharacter=r.containsNonAlphanumericCharacter),this.enforcementState=e.enforcementState,this.enforcementState==="ENFORCEMENT_STATE_UNSPECIFIED"&&(this.enforcementState="OFF"),this.allowedNonAlphanumericCharacters=((o=e.allowedNonAlphanumericCharacters)==null?void 0:o.join(""))??"",this.forceUpgradeOnSignin=e.forceUpgradeOnSignin??!1,this.schemaVersion=e.schemaVersion}validatePassword(e){const r={isValid:!0,passwordPolicy:this};return this.validatePasswordLengthOptions(e,r),this.validatePasswordCharacterOptions(e,r),r.isValid&&(r.isValid=r.meetsMinPasswordLength??!0),r.isValid&&(r.isValid=r.meetsMaxPasswordLength??!0),r.isValid&&(r.isValid=r.containsLowercaseLetter??!0),r.isValid&&(r.isValid=r.containsUppercaseLetter??!0),r.isValid&&(r.isValid=r.containsNumericCharacter??!0),r.isValid&&(r.isValid=r.containsNonAlphanumericCharacter??!0),r}validatePasswordLengthOptions(e,r){const o=this.customStrengthOptions.minPasswordLength,l=this.customStrengthOptions.maxPasswordLength;o&&(r.meetsMinPasswordLength=e.length>=o),l&&(r.meetsMaxPasswordLength=e.length<=l)}validatePasswordCharacterOptions(e,r){this.updatePasswordCharacterOptionsStatuses(r,!1,!1,!1,!1);let o;for(let l=0;l<e.length;l++)o=e.charAt(l),this.updatePasswordCharacterOptionsStatuses(r,o>="a"&&o<="z",o>="A"&&o<="Z",o>="0"&&o<="9",this.allowedNonAlphanumericCharacters.includes(o))}updatePasswordCharacterOptionsStatuses(e,r,o,l,c){this.customStrengthOptions.containsLowercaseLetter&&(e.containsLowercaseLetter||(e.containsLowercaseLetter=r)),this.customStrengthOptions.containsUppercaseLetter&&(e.containsUppercaseLetter||(e.containsUppercaseLetter=o)),this.customStrengthOptions.containsNumericCharacter&&(e.containsNumericCharacter||(e.containsNumericCharacter=l)),this.customStrengthOptions.containsNonAlphanumericCharacter&&(e.containsNonAlphanumericCharacter||(e.containsNonAlphanumericCharacter=c))}}/**
 * @license
 * Copyright 2020 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */class A1{constructor(e,r,o,l){this.app=e,this.heartbeatServiceProvider=r,this.appCheckServiceProvider=o,this.config=l,this.currentUser=null,this.emulatorConfig=null,this.operations=Promise.resolve(),this.authStateSubscription=new Yh(this),this.idTokenSubscription=new Yh(this),this.beforeStateQueue=new I1(this),this.redirectUser=null,this.isProactiveRefreshEnabled=!1,this.EXPECTED_PASSWORD_POLICY_SCHEMA_VERSION=1,this._canInitEmulator=!0,this._isInitialized=!1,this._deleted=!1,this._initializationPromise=null,this._popupRedirectResolver=null,this._errorFactory=kp,this._agentRecaptchaConfig=null,this._tenantRecaptchaConfigs={},this._projectPasswordPolicy=null,this._tenantPasswordPolicies={},this._resolvePersistenceManagerAvailable=void 0,this.lastNotifiedUid=void 0,this.languageCode=null,this.tenantId=null,this.settings={appVerificationDisabledForTesting:!1},this.frameworks=[],this.name=e.name,this.clientVersion=l.sdkClientVersion,this._persistenceManagerAvailable=new Promise(c=>this._resolvePersistenceManagerAvailable=c)}_initializeWithPersistence(e,r){return r&&(this._popupRedirectResolver=ar(r)),this._initializationPromise=this.queue(async()=>{var o,l,c;if(!this._deleted){try{this.persistenceManager=await li.create(this,e)}catch(h){na(`Failed to initialize persistence: ${h}`),this.persistenceManager=await li.create(this,[])}finally{(o=this._resolvePersistenceManagerAvailable)==null||o.call(this)}if(!this._deleted){if((l=this._popupRedirectResolver)!=null&&l._shouldInitProactively)try{await this._popupRedirectResolver._initialize(this)}catch{}try{await this.initializeCurrentUser(r)}catch(h){na(`Failed to initialize current user: ${h}`),await this.directlySetCurrentUser(null).catch(()=>{})}this.lastNotifiedUid=((c=this.currentUser)==null?void 0:c.uid)||null,!this._deleted&&(this._isInitialized=!0)}}}),this._initializationPromise}async _onStorageEvent(){if(this._deleted)return;const e=await this.assertedPersistence.getCurrentUser();if(!(!this.currentUser&&!e)){if(this.currentUser&&e&&this.currentUser.uid===e.uid){this._currentUser._assign(e),await this.currentUser.getIdToken();return}await this._updateCurrentUser(e,!0)}}async initializeCurrentUserFromIdToken(e){try{const r=await la(this,{idToken:e}),o=await Rn._fromGetAccountInfoResponse(this,r,e);await this.directlySetCurrentUser(o)}catch(r){console.warn("FirebaseServerApp could not login user with provided authIdToken: ",r),await this.directlySetCurrentUser(null)}}async initializeCurrentUser(e){var c;if(rn(this.app)){const h=this.app.settings.authIdToken;return h?new Promise(m=>{setTimeout(()=>this.initializeCurrentUserFromIdToken(h).then(m,m))}):this.directlySetCurrentUser(null)}const r=await this.assertedPersistence.getCurrentUser();let o=r,l=!1;if(e&&this.config.authDomain){await this.getOrInitRedirectPersistenceManager();const h=(c=this.redirectUser)==null?void 0:c._redirectEventId,m=o==null?void 0:o._redirectEventId,f=await this.tryRedirectSignIn(e);(!h||h===m)&&(f!=null&&f.user)&&(o=f.user,l=!0)}if(!o)return this.directlySetCurrentUser(null);if(!o._redirectEventId){if(l)try{await this.beforeStateQueue.runMiddleware(o)}catch(h){o=r,this._popupRedirectResolver._overrideRedirectResult(this,()=>Promise.reject(h))}return o?this.reloadAndSetCurrentUserOrClear(o):this.directlySetCurrentUser(null)}return Ee(this._popupRedirectResolver,this,"argument-error"),await this.getOrInitRedirectPersistenceManager(),this.redirectUser&&this.redirectUser._redirectEventId===o._redirectEventId?this.directlySetCurrentUser(o):this.reloadAndSetCurrentUserOrClear(o)}async tryRedirectSignIn(e){let r=null;try{r=await this._popupRedirectResolver._completeRedirectFn(this,e,!0)}catch{await this._setRedirectUser(null)}return r}async reloadAndSetCurrentUserOrClear(e){try{await ua(e)}catch(r){if(Np(r))return this.directlySetCurrentUser(null)}return this.directlySetCurrentUser(e)}useDeviceLanguage(){this.languageCode=c1()}async _delete(){this._deleted=!0}async updateCurrentUser(e){if(rn(this.app))return Promise.reject(jn(this));const r=e?Bn(e):null;return r&&Ee(r.auth.config.apiKey===this.config.apiKey,this,"invalid-user-token"),this._updateCurrentUser(r&&r._clone(this))}async _updateCurrentUser(e,r=!1){if(!this._deleted)return e&&Ee(this.tenantId===e.tenantId,this,"tenant-id-mismatch"),r||await this.beforeStateQueue.runMiddleware(e),this.queue(async()=>{await this.directlySetCurrentUser(e),this.notifyAuthListeners()})}async signOut(){return rn(this.app)?Promise.reject(jn(this)):(await this.beforeStateQueue.runMiddleware(null),(this.redirectPersistenceManager||this._popupRedirectResolver)&&await this._setRedirectUser(null),this._updateCurrentUser(null,!0))}setPersistence(e){return rn(this.app)?Promise.reject(jn(this)):this.queue(async()=>{await this.assertedPersistence.setPersistence(ar(e))})}_getRecaptchaConfig(){return this.tenantId==null?this._agentRecaptchaConfig:this._tenantRecaptchaConfigs[this.tenantId]}async validatePassword(e){this._getPasswordPolicyInternal()||await this._updatePasswordPolicy();const r=this._getPasswordPolicyInternal();return r.schemaVersion!==this.EXPECTED_PASSWORD_POLICY_SCHEMA_VERSION?Promise.reject(this._errorFactory.create("unsupported-password-policy-schema-version",{})):r.validatePassword(e)}_getPasswordPolicyInternal(){return this.tenantId===null?this._projectPasswordPolicy:this._tenantPasswordPolicies[this.tenantId]}async _updatePasswordPolicy(){const e=await R1(this),r=new P1(e);this.tenantId===null?this._projectPasswordPolicy=r:this._tenantPasswordPolicies[this.tenantId]=r}_getPersistenceType(){return this.assertedPersistence.persistence.type}_getPersistence(){return this.assertedPersistence.persistence}_updateErrorMap(e){this._errorFactory=new Fs("auth","Firebase",e())}onAuthStateChanged(e,r,o){return this.registerStateListener(this.authStateSubscription,e,r,o)}beforeAuthStateChanged(e,r){return this.beforeStateQueue.pushCallback(e,r)}onIdTokenChanged(e,r,o){return this.registerStateListener(this.idTokenSubscription,e,r,o)}authStateReady(){return new Promise((e,r)=>{if(this.currentUser)e();else{const o=this.onAuthStateChanged(()=>{o(),e()},r)}})}async revokeAccessToken(e){if(this.currentUser){const r=await this.currentUser.getIdToken(),o={providerId:"apple.com",tokenType:"ACCESS_TOKEN",token:e,idToken:r};this.tenantId!=null&&(o.tenantId=this.tenantId),await k1(this,o)}}toJSON(){var e;return{apiKey:this.config.apiKey,authDomain:this.config.authDomain,appName:this.name,currentUser:(e=this._currentUser)==null?void 0:e.toJSON()}}async _setRedirectUser(e,r){const o=await this.getOrInitRedirectPersistenceManager(r);return e===null?o.removeCurrentUser():o.setCurrentUser(e)}async getOrInitRedirectPersistenceManager(e){if(!this.redirectPersistenceManager){const r=e&&ar(e)||this._popupRedirectResolver;Ee(r,this,"argument-error"),this.redirectPersistenceManager=await li.create(this,[ar(r._redirectPersistence)],"redirectUser"),this.redirectUser=await this.redirectPersistenceManager.getCurrentUser()}return this.redirectPersistenceManager}async _redirectUserForId(e){var r,o;return this._isInitialized&&await this.queue(async()=>{}),((r=this._currentUser)==null?void 0:r._redirectEventId)===e?this._currentUser:((o=this.redirectUser)==null?void 0:o._redirectEventId)===e?this.redirectUser:null}async _persistUserIfCurrent(e){if(e===this.currentUser)return this.queue(async()=>this.directlySetCurrentUser(e))}_notifyListenersIfCurrent(e){e===this.currentUser&&this.notifyAuthListeners()}_key(){return`${this.config.authDomain}:${this.config.apiKey}:${this.name}`}_startProactiveRefresh(){this.isProactiveRefreshEnabled=!0,this.currentUser&&this._currentUser._startProactiveRefresh()}_stopProactiveRefresh(){this.isProactiveRefreshEnabled=!1,this.currentUser&&this._currentUser._stopProactiveRefresh()}get _currentUser(){return this.currentUser}notifyAuthListeners(){var r;if(!this._isInitialized)return;this.idTokenSubscription.next(this.currentUser);const e=((r=this.currentUser)==null?void 0:r.uid)??null;this.lastNotifiedUid!==e&&(this.lastNotifiedUid=e,this.authStateSubscription.next(this.currentUser))}registerStateListener(e,r,o,l){if(this._deleted)return()=>{};const c=typeof r=="function"?r:r.next.bind(r);let h=!1;const m=this._isInitialized?Promise.resolve():this._initializationPromise;if(Ee(m,this,"internal-error"),m.then(()=>{h||c(this.currentUser)}).catch(f=>{if(!h)if(typeof r!="function"&&r.error)r.error(f);else if(o)o(f);else throw f}),typeof r=="function"){const f=e.addObserver(r,o,l);return()=>{h=!0,f()}}else{const f=e.addObserver(r);return()=>{h=!0,f()}}}async directlySetCurrentUser(e){if(this.currentUser&&this.currentUser!==e&&this._currentUser._stopProactiveRefresh(),e&&this.isProactiveRefreshEnabled&&e._startProactiveRefresh(),this.currentUser=e,this.persistenceManager)try{e?await this.persistenceManager.setCurrentUser(e):await this.persistenceManager.removeCurrentUser()}catch(r){const o=(r==null?void 0:r.message)||String(r),l=ga(this,"internal-error",`An internal AuthError has occurred: ${o}`);throw l.customData={originalError:r},l}}queue(e){return this.operations=this.operations.then(e,e),this.operations}get assertedPersistence(){return Ee(this.persistenceManager,this,"internal-error"),this.persistenceManager}_logFramework(e){!e||this.frameworks.includes(e)||(this.frameworks.push(e),this.frameworks.sort(),this.clientVersion=Up(this.config.clientPlatform,this._getFrameworks()))}_getFrameworks(){return this.frameworks}async _getAdditionalHeaders(){var l;const e={"X-Client-Version":this.clientVersion};this.app.options.appId&&(e["X-Firebase-gmpid"]=this.app.options.appId);const r=await((l=this.heartbeatServiceProvider.getImmediate({optional:!0}))==null?void 0:l.getHeartbeatsHeader());r&&(e["X-Firebase-Client"]=r);const o=await this._getAppCheckToken();return o&&(e["X-Firebase-AppCheck"]=o),e}async _getAppCheckToken(){var r;if(rn(this.app)&&this.app.settings.appCheckToken)return this.app.settings.appCheckToken;const e=await((r=this.appCheckServiceProvider.getImmediate({optional:!0}))==null?void 0:r.getToken());return e!=null&&e.error&&na(`Error while retrieving App Check token: ${e.error}`),e==null?void 0:e.token}}function Vn(i){return Bn(i)}class Yh{constructor(e){this.auth=e,this.observer=null,this.addObserver=G0(r=>this.observer=r)}get next(){return Ee(this.observer,this.auth,"internal-error"),this.observer.next.bind(this.observer)}}/**
 * @license
 * Copyright 2020 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */let va={async loadJS(){throw new Error("Unable to load external scripts")},recaptchaV2Script:"",recaptchaEnterpriseScript:"",gapiScript:""};function M1(i){va=i}function Bp(i){return va.loadJS(i)}function D1(){return va.recaptchaEnterpriseScript}function b1(){return va.gapiScript}function L1(i){return`__${i}${Math.floor(Math.random()*1e6)}`}class O1{constructor(){this.enterprise=new F1}ready(e){e()}execute(e,r){return Promise.resolve("token")}render(e,r){return""}}class F1{ready(e){e()}execute(e,r){return Promise.resolve("token")}render(e,r){return""}}/**
 * @license
 * Copyright 2022 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */const z1="recaptcha-enterprise",$p="NO_RECAPTCHA",Qh="onFirebaseAuthREInstanceReady";class Lr{constructor(e){this.type=z1,this.auth=Vn(e)}async verify(e="verify",r=!1){async function o(c){if(!r){if(c.tenantId==null&&c._agentRecaptchaConfig!=null)return c._agentRecaptchaConfig.siteKey;if(c.tenantId!=null&&c._tenantRecaptchaConfigs[c.tenantId]!==void 0)return c._tenantRecaptchaConfigs[c.tenantId].siteKey}return new Promise(async(h,m)=>{v1(c,{clientType:"CLIENT_TYPE_WEB",version:"RECAPTCHA_ENTERPRISE"}).then(f=>{if(f.recaptchaKey===void 0)m(new Error("recaptcha Enterprise site key undefined"));else{const v=new g1(f);return c.tenantId==null?c._agentRecaptchaConfig=v:c._tenantRecaptchaConfigs[c.tenantId]=v,h(v.siteKey)}}).catch(f=>{m(f)})})}function l(c,h,m){const f=window.grecaptcha;Wh(f)?f.enterprise.ready(()=>{f.enterprise.execute(c,{action:e}).then(v=>{h(v)}).catch(()=>{h($p)})}):m(Error("No reCAPTCHA enterprise script loaded."))}return this.auth.settings.appVerificationDisabledForTesting?new O1().execute("siteKey",{action:"verify"}):new Promise((c,h)=>{o(this.auth).then(async m=>{if(!r&&Wh(window.grecaptcha)&&Lr.scriptInjectionDeferred)await Lr.scriptInjectionDeferred.promise,l(m,c,h);else{if(typeof window>"u"){h(new Error("RecaptchaVerifier is only supported in browser"));return}let f=D1();f.length!==0&&(f+=m+`&onload=${Qh}`),Lr.scriptInjectionDeferred=new pp,window[Qh]=()=>{var v;(v=Lr.scriptInjectionDeferred)==null||v.resolve()},Bp(f).then(()=>{var v;return(v=Lr.scriptInjectionDeferred)==null?void 0:v.promise}).then(()=>{l(m,c,h)}).catch(v=>{h(v)})}}).catch(m=>{h(m)})})}}Lr.scriptInjectionDeferred=null;async function Jh(i,e,r,o=!1,l=!1){const c=new Lr(i);let h;if(l)h=$p;else try{h=await c.verify(r)}catch{h=await c.verify(r,!0)}const m={...e};if(r==="mfaSmsEnrollment"||r==="mfaSmsSignIn"){if("phoneEnrollmentInfo"in m){const f=m.phoneEnrollmentInfo.phoneNumber,v=m.phoneEnrollmentInfo.recaptchaToken;Object.assign(m,{phoneEnrollmentInfo:{phoneNumber:f,recaptchaToken:v,captchaResponse:h,clientType:"CLIENT_TYPE_WEB",recaptchaVersion:"RECAPTCHA_ENTERPRISE"}})}else if("phoneSignInInfo"in m){const f=m.phoneSignInInfo.recaptchaToken;Object.assign(m,{phoneSignInInfo:{recaptchaToken:f,captchaResponse:h,clientType:"CLIENT_TYPE_WEB",recaptchaVersion:"RECAPTCHA_ENTERPRISE"}})}return m}return o?Object.assign(m,{captchaResp:h}):Object.assign(m,{captchaResponse:h}),Object.assign(m,{clientType:"CLIENT_TYPE_WEB"}),Object.assign(m,{recaptchaVersion:"RECAPTCHA_ENTERPRISE"}),m}async function ca(i,e,r,o,l){var c;if((c=i._getRecaptchaConfig())!=null&&c.isProviderEnabled("EMAIL_PASSWORD_PROVIDER")){const h=await Jh(i,e,r,r==="getOobCode");return o(i,h)}else return o(i,e).catch(async h=>{if(h.code==="auth/missing-recaptcha-token"){console.log(`${r} is protected by reCAPTCHA Enterprise for this project. Automatically triggering the reCAPTCHA flow and restarting the flow.`);const m=await Jh(i,e,r,r==="getOobCode");return o(i,m)}else return Promise.reject(h)})}/**
 * @license
 * Copyright 2020 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */function j1(i,e){const r=yp(i,"auth");if(r.isInitialized()){const l=r.getImmediate(),c=r.getOptions();if($i(c,e??{}))return l;vn(l,"already-initialized")}return r.initialize({options:e})}function U1(i,e){const r=(e==null?void 0:e.persistence)||[],o=(Array.isArray(r)?r:[r]).map(ar);e!=null&&e.errorMap&&i._updateErrorMap(e.errorMap),i._initializeWithPersistence(o,e==null?void 0:e.popupRedirectResolver)}function B1(i,e,r){const o=Vn(i);Ee(/^https?:\/\//.test(e),o,"invalid-emulator-scheme");const l=!1,c=Vp(e),{host:h,port:m}=$1(e),f=m===null?"":`:${m}`,v={url:`${c}//${h}${f}/`},x=Object.freeze({host:h,port:m,protocol:c.replace(":",""),options:Object.freeze({disableWarnings:l})});if(!o._canInitEmulator){Ee(o.config.emulator&&o.emulatorConfig,o,"emulator-config-failed"),Ee($i(v,o.config.emulator)&&$i(x,o.emulatorConfig),o,"emulator-config-failed");return}o.config.emulator=v,o.emulatorConfig=x,o.settings.appVerificationDisabledForTesting=!0,Lu(h)?X0(`${c}//${h}${f}`):V1()}function Vp(i){const e=i.indexOf(":");return e<0?"":i.substr(0,e+1)}function $1(i){const e=Vp(i),r=/(\/\/)?([^?#/]+)/.exec(i.substr(e.length));if(!r)return{host:"",port:null};const o=r[2].split("@").pop()||"",l=/^(\[[^\]]+\])(:|$)/.exec(o);if(l){const c=l[1];return{host:c,port:Zh(o.substr(c.length+1))}}else{const[c,h]=o.split(":");return{host:c,port:Zh(h)}}}function Zh(i){if(!i)return null;const e=Number(i);return isNaN(e)?null:e}function V1(){function i(){const e=document.createElement("p"),r=e.style;e.innerText="Running in emulator mode. Do not use with production credentials.",r.position="fixed",r.width="100%",r.backgroundColor="#ffffff",r.border=".1em solid #000000",r.color="#b50000",r.bottom="0px",r.left="0px",r.margin="0px",r.zIndex="10000",r.textAlign="center",e.classList.add("firebase-emulator-warning"),document.body.appendChild(e)}typeof console<"u"&&typeof console.info=="function"&&console.info("WARNING: You are using the Auth Emulator, which is intended for local testing only.  Do not use with production credentials."),typeof window<"u"&&typeof document<"u"&&(document.readyState==="loading"?window.addEventListener("DOMContentLoaded",i):i())}/**
 * @license
 * Copyright 2020 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */class Bu{constructor(e,r){this.providerId=e,this.signInMethod=r}toJSON(){return or("not implemented")}_getIdTokenResponse(e){return or("not implemented")}_linkToIdToken(e,r){return or("not implemented")}_getReauthenticationResolver(e){return or("not implemented")}}async function H1(i,e){return $n(i,"POST","/v1/accounts:signUp",e)}/**
 * @license
 * Copyright 2020 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */async function W1(i,e){return Bs(i,"POST","/v1/accounts:signInWithPassword",cr(i,e))}async function G1(i,e){return $n(i,"POST","/v1/accounts:sendOobCode",cr(i,e))}async function q1(i,e){return G1(i,e)}/**
 * @license
 * Copyright 2020 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */async function K1(i,e){return Bs(i,"POST","/v1/accounts:signInWithEmailLink",cr(i,e))}async function X1(i,e){return Bs(i,"POST","/v1/accounts:signInWithEmailLink",cr(i,e))}/**
 * @license
 * Copyright 2020 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */class Ls extends Bu{constructor(e,r,o,l=null){super("password",o),this._email=e,this._password=r,this._tenantId=l}static _fromEmailAndPassword(e,r){return new Ls(e,r,"password")}static _fromEmailAndCode(e,r,o=null){return new Ls(e,r,"emailLink",o)}toJSON(){return{email:this._email,password:this._password,signInMethod:this.signInMethod,tenantId:this._tenantId}}static fromJSON(e){const r=typeof e=="string"?JSON.parse(e):e;if(r!=null&&r.email&&(r!=null&&r.password)){if(r.signInMethod==="password")return this._fromEmailAndPassword(r.email,r.password);if(r.signInMethod==="emailLink")return this._fromEmailAndCode(r.email,r.password,r.tenantId)}return null}async _getIdTokenResponse(e){switch(this.signInMethod){case"password":const r={returnSecureToken:!0,email:this._email,password:this._password,clientType:"CLIENT_TYPE_WEB"};return ca(e,r,"signInWithPassword",W1);case"emailLink":return K1(e,{email:this._email,oobCode:this._password});default:vn(e,"internal-error")}}async _linkToIdToken(e,r){switch(this.signInMethod){case"password":const o={idToken:r,returnSecureToken:!0,email:this._email,password:this._password,clientType:"CLIENT_TYPE_WEB"};return ca(e,o,"signUpPassword",H1);case"emailLink":return X1(e,{idToken:r,email:this._email,oobCode:this._password});default:vn(e,"internal-error")}}_getReauthenticationResolver(e){return this._getIdTokenResponse(e)}}/**
 * @license
 * Copyright 2020 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */async function Bi(i,e){return Bs(i,"POST","/v1/accounts:signInWithIdp",cr(i,e))}/**
 * @license
 * Copyright 2020 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */const Y1="http://localhost";class ui extends Bu{constructor(){super(...arguments),this.pendingToken=null}static _fromParams(e){const r=new ui(e.providerId,e.signInMethod);return e.idToken||e.accessToken?(e.idToken&&(r.idToken=e.idToken),e.accessToken&&(r.accessToken=e.accessToken),e.nonce&&!e.pendingToken&&(r.nonce=e.nonce),e.pendingToken&&(r.pendingToken=e.pendingToken)):e.oauthToken&&e.oauthTokenSecret?(r.accessToken=e.oauthToken,r.secret=e.oauthTokenSecret):vn("argument-error"),r}toJSON(){return{idToken:this.idToken,accessToken:this.accessToken,secret:this.secret,nonce:this.nonce,pendingToken:this.pendingToken,providerId:this.providerId,signInMethod:this.signInMethod}}static fromJSON(e){const r=typeof e=="string"?JSON.parse(e):e,{providerId:o,signInMethod:l,...c}=r;if(!o||!l)return null;const h=new ui(o,l);return h.idToken=c.idToken||void 0,h.accessToken=c.accessToken||void 0,h.secret=c.secret,h.nonce=c.nonce,h.pendingToken=c.pendingToken||null,h}_getIdTokenResponse(e){const r=this.buildRequest();return Bi(e,r)}_linkToIdToken(e,r){const o=this.buildRequest();return o.idToken=r,Bi(e,o)}_getReauthenticationResolver(e){const r=this.buildRequest();return r.autoCreate=!1,Bi(e,r)}buildRequest(){const e={requestUri:Y1,returnSecureToken:!0};if(this.pendingToken)e.pendingToken=this.pendingToken;else{const r={};this.idToken&&(r.id_token=this.idToken),this.accessToken&&(r.access_token=this.accessToken),this.secret&&(r.oauth_token_secret=this.secret),r.providerId=this.providerId,this.nonce&&!this.pendingToken&&(r.nonce=this.nonce),e.postBody=zs(r)}return e}}/**
 * @license
 * Copyright 2020 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */function Q1(i){switch(i){case"recoverEmail":return"RECOVER_EMAIL";case"resetPassword":return"PASSWORD_RESET";case"signIn":return"EMAIL_SIGNIN";case"verifyEmail":return"VERIFY_EMAIL";case"verifyAndChangeEmail":return"VERIFY_AND_CHANGE_EMAIL";case"revertSecondFactorAddition":return"REVERT_SECOND_FACTOR_ADDITION";default:return null}}function J1(i){const e=Rs(Ns(i)).link,r=e?Rs(Ns(e)).deep_link_id:null,o=Rs(Ns(i)).deep_link_id;return(o?Rs(Ns(o)).link:null)||o||r||e||i}class $u{constructor(e){const r=Rs(Ns(e)),o=r.apiKey??null,l=r.oobCode??null,c=Q1(r.mode??null);Ee(o&&l&&c,"argument-error"),this.apiKey=o,this.operation=c,this.code=l,this.continueUrl=r.continueUrl??null,this.languageCode=r.lang??null,this.tenantId=r.tenantId??null}static parseLink(e){const r=J1(e);try{return new $u(r)}catch{return null}}}/**
 * @license
 * Copyright 2020 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */class Wi{constructor(){this.providerId=Wi.PROVIDER_ID}static credential(e,r){return Ls._fromEmailAndPassword(e,r)}static credentialWithLink(e,r){const o=$u.parseLink(r);return Ee(o,"argument-error"),Ls._fromEmailAndCode(e,o.code,o.tenantId)}}Wi.PROVIDER_ID="password";Wi.EMAIL_PASSWORD_SIGN_IN_METHOD="password";Wi.EMAIL_LINK_SIGN_IN_METHOD="emailLink";/**
 * @license
 * Copyright 2020 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */class ya{constructor(e){this.providerId=e,this.defaultLanguageCode=null,this.customParameters={}}setDefaultLanguage(e){this.defaultLanguageCode=e}setCustomParameters(e){return this.customParameters=e,this}getCustomParameters(){return this.customParameters}}/**
 * @license
 * Copyright 2019 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */class $s extends ya{constructor(){super(...arguments),this.scopes=[]}addScope(e){return this.scopes.includes(e)||this.scopes.push(e),this}getScopes(){return[...this.scopes]}}/**
 * @license
 * Copyright 2020 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */class Or extends $s{constructor(){super("facebook.com")}static credential(e){return ui._fromParams({providerId:Or.PROVIDER_ID,signInMethod:Or.FACEBOOK_SIGN_IN_METHOD,accessToken:e})}static credentialFromResult(e){return Or.credentialFromTaggedObject(e)}static credentialFromError(e){return Or.credentialFromTaggedObject(e.customData||{})}static credentialFromTaggedObject({_tokenResponse:e}){if(!e||!("oauthAccessToken"in e)||!e.oauthAccessToken)return null;try{return Or.credential(e.oauthAccessToken)}catch{return null}}}Or.FACEBOOK_SIGN_IN_METHOD="facebook.com";Or.PROVIDER_ID="facebook.com";/**
 * @license
 * Copyright 2020 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */class rr extends $s{constructor(){super("google.com"),this.addScope("profile")}static credential(e,r){return ui._fromParams({providerId:rr.PROVIDER_ID,signInMethod:rr.GOOGLE_SIGN_IN_METHOD,idToken:e,accessToken:r})}static credentialFromResult(e){return rr.credentialFromTaggedObject(e)}static credentialFromError(e){return rr.credentialFromTaggedObject(e.customData||{})}static credentialFromTaggedObject({_tokenResponse:e}){if(!e)return null;const{oauthIdToken:r,oauthAccessToken:o}=e;if(!r&&!o)return null;try{return rr.credential(r,o)}catch{return null}}}rr.GOOGLE_SIGN_IN_METHOD="google.com";rr.PROVIDER_ID="google.com";/**
 * @license
 * Copyright 2020 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */class Fr extends $s{constructor(){super("github.com")}static credential(e){return ui._fromParams({providerId:Fr.PROVIDER_ID,signInMethod:Fr.GITHUB_SIGN_IN_METHOD,accessToken:e})}static credentialFromResult(e){return Fr.credentialFromTaggedObject(e)}static credentialFromError(e){return Fr.credentialFromTaggedObject(e.customData||{})}static credentialFromTaggedObject({_tokenResponse:e}){if(!e||!("oauthAccessToken"in e)||!e.oauthAccessToken)return null;try{return Fr.credential(e.oauthAccessToken)}catch{return null}}}Fr.GITHUB_SIGN_IN_METHOD="github.com";Fr.PROVIDER_ID="github.com";/**
 * @license
 * Copyright 2020 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */class zr extends $s{constructor(){super("twitter.com")}static credential(e,r){return ui._fromParams({providerId:zr.PROVIDER_ID,signInMethod:zr.TWITTER_SIGN_IN_METHOD,oauthToken:e,oauthTokenSecret:r})}static credentialFromResult(e){return zr.credentialFromTaggedObject(e)}static credentialFromError(e){return zr.credentialFromTaggedObject(e.customData||{})}static credentialFromTaggedObject({_tokenResponse:e}){if(!e)return null;const{oauthAccessToken:r,oauthTokenSecret:o}=e;if(!r||!o)return null;try{return zr.credential(r,o)}catch{return null}}}zr.TWITTER_SIGN_IN_METHOD="twitter.com";zr.PROVIDER_ID="twitter.com";/**
 * @license
 * Copyright 2020 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */async function Z1(i,e){return Bs(i,"POST","/v1/accounts:signUp",cr(i,e))}/**
 * @license
 * Copyright 2020 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */class ci{constructor(e){this.user=e.user,this.providerId=e.providerId,this._tokenResponse=e._tokenResponse,this.operationType=e.operationType}static async _fromIdTokenResponse(e,r,o,l=!1){const c=await Rn._fromIdTokenResponse(e,o,l),h=ef(o);return new ci({user:c,providerId:h,_tokenResponse:o,operationType:r})}static async _forOperation(e,r,o){await e._updateTokensIfNecessary(o,!0);const l=ef(o);return new ci({user:e,providerId:l,_tokenResponse:o,operationType:r})}}function ef(i){return i.providerId?i.providerId:"phoneNumber"in i?"phone":null}/**
 * @license
 * Copyright 2020 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */class da extends Br{constructor(e,r,o,l){super(r.code,r.message),this.operationType=o,this.user=l,Object.setPrototypeOf(this,da.prototype),this.customData={appName:e.name,tenantId:e.tenantId??void 0,_serverResponse:r.customData._serverResponse,operationType:o}}static _fromErrorAndOperation(e,r,o,l){return new da(e,r,o,l)}}function Hp(i,e,r,o){return(e==="reauthenticate"?r._getReauthenticationResolver(i):r._getIdTokenResponse(i)).catch(c=>{throw c.code==="auth/multi-factor-auth-required"?da._fromErrorAndOperation(i,c,e,o):c})}async function ey(i,e,r=!1){const o=await Hi(i,e._linkToIdToken(i.auth,await i.getIdToken()),r);return ci._forOperation(i,"link",o)}/**
 * @license
 * Copyright 2019 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */async function ty(i,e,r=!1){const{auth:o}=i;if(rn(o.app))return Promise.reject(jn(o));const l="reauthenticate";try{const c=await Hi(i,Hp(o,l,e,i),r);Ee(c.idToken,o,"internal-error");const h=ju(c.idToken);Ee(h,o,"internal-error");const{sub:m}=h;return Ee(i.uid===m,o,"user-mismatch"),ci._forOperation(i,l,c)}catch(c){throw(c==null?void 0:c.code)==="auth/user-not-found"&&vn(o,"user-mismatch"),c}}/**
 * @license
 * Copyright 2020 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */async function Wp(i,e,r=!1){if(rn(i.app))return Promise.reject(jn(i));const o="signIn",l=await Hp(i,o,e),c=await ci._fromIdTokenResponse(i,o,l);return r||await i._updateCurrentUser(c.user),c}async function ny(i,e){return Wp(Vn(i),e)}/**
 * @license
 * Copyright 2020 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */async function Gp(i){const e=Vn(i);e._getPasswordPolicyInternal()&&await e._updatePasswordPolicy()}async function ry(i,e,r){const o=Vn(i);await ca(o,{requestType:"PASSWORD_RESET",email:e,clientType:"CLIENT_TYPE_WEB"},"getOobCode",q1)}async function iy(i,e,r){if(rn(i.app))return Promise.reject(jn(i));const o=Vn(i),h=await ca(o,{returnSecureToken:!0,email:e,password:r,clientType:"CLIENT_TYPE_WEB"},"signUpPassword",Z1).catch(f=>{throw f.code==="auth/password-does-not-meet-requirements"&&Gp(i),f}),m=await ci._fromIdTokenResponse(o,"signIn",h);return await o._updateCurrentUser(m.user),m}function sy(i,e,r){return rn(i.app)?Promise.reject(jn(i)):ny(Bn(i),Wi.credential(e,r)).catch(async o=>{throw o.code==="auth/password-does-not-meet-requirements"&&Gp(i),o})}/**
 * @license
 * Copyright 2020 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */async function oy(i,e){return $n(i,"POST","/v1/accounts:update",e)}/**
 * @license
 * Copyright 2020 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */async function ay(i,e){const{displayName:r,photoURL:o}=e;if(r===void 0&&o===void 0)return;const l=Bn(i),h={idToken:await l.getIdToken(),displayName:r,photoUrl:o,returnSecureToken:!0},m=await Hi(l,oy(l.auth,h));l.displayName=m.displayName||null,l.photoURL=m.photoUrl||null;const f=l.providerData.find(({providerId:v})=>v==="password");f&&(f.displayName=l.displayName,f.photoURL=l.photoURL),await l._updateTokensIfNecessary(m)}function ly(i,e,r,o){return Bn(i).onIdTokenChanged(e,r,o)}function uy(i,e,r){return Bn(i).beforeAuthStateChanged(e,r)}function cy(i,e,r,o){return Bn(i).onAuthStateChanged(e,r,o)}function dy(i){return Bn(i).signOut()}const ha="__sak";/**
 * @license
 * Copyright 2019 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */class qp{constructor(e,r){this.storageRetriever=e,this.type=r}_isAvailable(){try{return this.storage?(this.storage.setItem(ha,"1"),this.storage.removeItem(ha),Promise.resolve(!0)):Promise.resolve(!1)}catch{return Promise.resolve(!1)}}_set(e,r){return this.storage.setItem(e,JSON.stringify(r)),Promise.resolve()}_get(e){const r=this.storage.getItem(e);return Promise.resolve(r?JSON.parse(r):null)}_remove(e){return this.storage.removeItem(e),Promise.resolve()}get storage(){return this.storageRetriever()}}/**
 * @license
 * Copyright 2020 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */const hy=1e3,fy=10;class Kp extends qp{constructor(){super(()=>window.localStorage,"LOCAL"),this.boundEventHandler=(e,r)=>this.onStorageEvent(e,r),this.listeners={},this.localCache={},this.pollTimer=null,this.fallbackToPolling=jp(),this._shouldAllowMigration=!0}forAllChangedKeys(e){for(const r of Object.keys(this.listeners)){const o=this.storage.getItem(r),l=this.localCache[r];o!==l&&e(r,l,o)}}onStorageEvent(e,r=!1){if(!e.key){this.forAllChangedKeys((h,m,f)=>{this.notifyListeners(h,f)});return}const o=e.key;r?this.detachListener():this.stopPolling();const l=()=>{const h=this.storage.getItem(o);!r&&this.localCache[o]===h||this.notifyListeners(o,h)},c=this.storage.getItem(o);C1()&&c!==e.newValue&&e.newValue!==e.oldValue?setTimeout(l,fy):l()}notifyListeners(e,r){this.localCache[e]=r;const o=this.listeners[e];if(o)for(const l of Array.from(o))l(r&&JSON.parse(r))}startPolling(){this.stopPolling(),this.pollTimer=setInterval(()=>{this.forAllChangedKeys((e,r,o)=>{this.onStorageEvent(new StorageEvent("storage",{key:e,oldValue:r,newValue:o}),!0)})},hy)}stopPolling(){this.pollTimer&&(clearInterval(this.pollTimer),this.pollTimer=null)}attachListener(){window.addEventListener("storage",this.boundEventHandler)}detachListener(){window.removeEventListener("storage",this.boundEventHandler)}_addListener(e,r){Object.keys(this.listeners).length===0&&(this.fallbackToPolling?this.startPolling():this.attachListener()),this.listeners[e]||(this.listeners[e]=new Set,this.localCache[e]=this.storage.getItem(e)),this.listeners[e].add(r)}_removeListener(e,r){this.listeners[e]&&(this.listeners[e].delete(r),this.listeners[e].size===0&&delete this.listeners[e]),Object.keys(this.listeners).length===0&&(this.detachListener(),this.stopPolling())}async _set(e,r){await super._set(e,r),this.localCache[e]=JSON.stringify(r)}async _get(e){const r=await super._get(e);return this.localCache[e]=JSON.stringify(r),r}async _remove(e){await super._remove(e),delete this.localCache[e]}}Kp.type="LOCAL";const py=Kp;/**
 * @license
 * Copyright 2020 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */class Xp extends qp{constructor(){super(()=>window.sessionStorage,"SESSION")}_addListener(e,r){}_removeListener(e,r){}}Xp.type="SESSION";const Yp=Xp;/**
 * @license
 * Copyright 2019 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */function my(i){return Promise.all(i.map(async e=>{try{return{fulfilled:!0,value:await e}}catch(r){return{fulfilled:!1,reason:r}}}))}/**
 * @license
 * Copyright 2019 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */class wa{constructor(e){this.eventTarget=e,this.handlersMap={},this.boundEventHandler=this.handleEvent.bind(this)}static _getInstance(e){const r=this.receivers.find(l=>l.isListeningto(e));if(r)return r;const o=new wa(e);return this.receivers.push(o),o}isListeningto(e){return this.eventTarget===e}async handleEvent(e){const r=e,{eventId:o,eventType:l,data:c}=r.data,h=this.handlersMap[l];if(!(h!=null&&h.size))return;r.ports[0].postMessage({status:"ack",eventId:o,eventType:l});const m=Array.from(h).map(async v=>v(r.origin,c)),f=await my(m);r.ports[0].postMessage({status:"done",eventId:o,eventType:l,response:f})}_subscribe(e,r){Object.keys(this.handlersMap).length===0&&this.eventTarget.addEventListener("message",this.boundEventHandler),this.handlersMap[e]||(this.handlersMap[e]=new Set),this.handlersMap[e].add(r)}_unsubscribe(e,r){this.handlersMap[e]&&r&&this.handlersMap[e].delete(r),(!r||this.handlersMap[e].size===0)&&delete this.handlersMap[e],Object.keys(this.handlersMap).length===0&&this.eventTarget.removeEventListener("message",this.boundEventHandler)}}wa.receivers=[];/**
 * @license
 * Copyright 2020 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */function Vu(i="",e=10){let r="";for(let o=0;o<e;o++)r+=Math.floor(Math.random()*10);return i+r}/**
 * @license
 * Copyright 2019 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */class gy{constructor(e){this.target=e,this.handlers=new Set}removeMessageHandler(e){e.messageChannel&&(e.messageChannel.port1.removeEventListener("message",e.onMessage),e.messageChannel.port1.close()),this.handlers.delete(e)}async _send(e,r,o=50){const l=typeof MessageChannel<"u"?new MessageChannel:null;if(!l)throw new Error("connection_unavailable");let c,h;return new Promise((m,f)=>{const v=Vu("",20);l.port1.start();const x=setTimeout(()=>{f(new Error("unsupported_event"))},o);h={messageChannel:l,onMessage(S){const T=S;if(T.data.eventId===v)switch(T.data.status){case"ack":clearTimeout(x),c=setTimeout(()=>{f(new Error("timeout"))},3e3);break;case"done":clearTimeout(c),m(T.data.response);break;default:clearTimeout(x),clearTimeout(c),f(new Error("invalid_response"));break}}},this.handlers.add(h),l.port1.addEventListener("message",h.onMessage),this.target.postMessage({eventType:e,eventId:v,data:r},[l.port2])}).finally(()=>{h&&this.removeMessageHandler(h)})}}/**
 * @license
 * Copyright 2020 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */function Un(){return window}function vy(i){Un().location.href=i}/**
 * @license
 * Copyright 2020 Google LLC.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */function Qp(){return typeof Un().WorkerGlobalScope<"u"&&typeof Un().importScripts=="function"}async function yy(){if(!(navigator!=null&&navigator.serviceWorker))return null;try{return(await navigator.serviceWorker.ready).active}catch{return null}}function wy(){var i;return((i=navigator==null?void 0:navigator.serviceWorker)==null?void 0:i.controller)||null}function xy(){return Qp()?self:null}/**
 * @license
 * Copyright 2019 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */const Jp="firebaseLocalStorageDb",_y=1,fa="firebaseLocalStorage",Zp="fbase_key";class Vs{constructor(e){this.request=e}toPromise(){return new Promise((e,r)=>{this.request.addEventListener("success",()=>{e(this.request.result)}),this.request.addEventListener("error",()=>{r(this.request.error)})})}}function xa(i,e){return i.transaction([fa],e?"readwrite":"readonly").objectStore(fa)}function Ey(){const i=indexedDB.deleteDatabase(Jp);return new Vs(i).toPromise()}function em(){const i=indexedDB.open(Jp,_y);return new Promise((e,r)=>{i.addEventListener("error",()=>{r(i.error)}),i.addEventListener("upgradeneeded",()=>{const o=i.result;try{o.createObjectStore(fa,{keyPath:Zp})}catch(l){r(l)}}),i.addEventListener("success",async()=>{const o=i.result;o.objectStoreNames.contains(fa)?e(o):(o.close(),await Ey(),e(await em()))})})}async function tf(i,e,r){const o=xa(i,!0).put({[Zp]:e,value:r});return new Vs(o).toPromise()}async function Sy(i,e){const r=xa(i,!1).get(e),o=await new Vs(r).toPromise();return o===void 0?null:o.value}function nf(i,e){const r=xa(i,!0).delete(e);return new Vs(r).toPromise()}const ky=800,Ty=3;class tm{registerLifecycleListeners(){typeof window<"u"&&typeof window.addEventListener=="function"&&(window.addEventListener("pagehide",this.onPageHide),window.addEventListener("pageshow",this.onPageShow))}unregisterLifecycleListeners(){typeof window<"u"&&typeof window.removeEventListener=="function"&&(window.removeEventListener("pagehide",this.onPageHide),window.removeEventListener("pageshow",this.onPageShow))}constructor(){this.type="LOCAL",this.dbPromise=null,this._shouldAllowMigration=!0,this.listeners={},this.localCache={},this.pollTimer=null,this.isClosing=!1,this.pendingWrites=0,this.receiver=null,this.sender=null,this.serviceWorkerReceiverAvailable=!1,this.activeServiceWorker=null,this.onPageHide=()=>{this.isClosing=!0,this.stopPolling(),this.dbPromise&&(this.dbPromise.then(e=>e.close()).catch(()=>{}),this.dbPromise=null)},this.onPageShow=()=>{this.isClosing&&(this.isClosing=!1,Object.keys(this.listeners).length>0&&this.startPolling())},this._workerInitializationPromise=this.initializeServiceWorkerMessaging().then(()=>{},()=>{})}async _openDb(){return this.dbPromise?this.dbPromise:(this.dbPromise=em(),this.dbPromise.catch(()=>{this.dbPromise=null}),this.dbPromise)}async _withRetries(e){let r=0;for(;;)try{const o=await this._openDb();return await e(o)}catch(o){if(r++>Ty)throw o;if(this.dbPromise){const l=this.dbPromise;this.dbPromise=null;try{(await l).close()}catch{}}}}async initializeServiceWorkerMessaging(){return Qp()?this.initializeReceiver():this.initializeSender()}async initializeReceiver(){this.receiver=wa._getInstance(xy()),this.receiver._subscribe("keyChanged",async(e,r)=>({keyProcessed:(await this._poll()).includes(r.key)})),this.receiver._subscribe("ping",async(e,r)=>["keyChanged"])}async initializeSender(){var r,o;if(this.activeServiceWorker=await yy(),!this.activeServiceWorker)return;this.sender=new gy(this.activeServiceWorker);const e=await this.sender._send("ping",{},800);e&&(r=e[0])!=null&&r.fulfilled&&(o=e[0])!=null&&o.value.includes("keyChanged")&&(this.serviceWorkerReceiverAvailable=!0)}async notifyServiceWorker(e){if(!(!this.sender||!this.activeServiceWorker||wy()!==this.activeServiceWorker))try{await this.sender._send("keyChanged",{key:e},this.serviceWorkerReceiverAvailable?800:50)}catch{}}async _isAvailable(){try{return indexedDB?(await this._withRetries(async e=>{await tf(e,ha,"1"),await nf(e,ha)}),!0):!1}catch{}return!1}async _withPendingWrite(e){this.pendingWrites++;try{await e()}finally{this.pendingWrites--}}async _set(e,r){return this._withPendingWrite(async()=>(await this._withRetries(o=>tf(o,e,r)),this.localCache[e]=r,this.notifyServiceWorker(e)))}async _get(e){const r=await this._withRetries(o=>Sy(o,e));return this.localCache[e]=r,r}async _remove(e){return this._withPendingWrite(async()=>(await this._withRetries(r=>nf(r,e)),delete this.localCache[e],this.notifyServiceWorker(e)))}async _poll(){if(this.isClosing)return[];try{const e=await this._withRetries(l=>{const c=xa(l,!1).getAll();return new Vs(c).toPromise()});if(this.isClosing)return[];if(!e)return[];if(this.pendingWrites!==0)return[];const r=[],o=new Set;if(e.length!==0)for(const{fbase_key:l,value:c}of e)o.add(l),JSON.stringify(this.localCache[l])!==JSON.stringify(c)&&(this.notifyListeners(l,c),r.push(l));for(const l of Object.keys(this.localCache))this.localCache[l]&&!o.has(l)&&(this.notifyListeners(l,null),r.push(l));return r}catch(e){return this.isClosing||na(`Firebase Auth cross-tab polling failed with error: ${e}`),[]}}notifyListeners(e,r){this.localCache[e]=r;const o=this.listeners[e];if(o)for(const l of Array.from(o))l(r)}startPolling(){this.stopPolling(),this.pollTimer=setInterval(async()=>this._poll(),ky)}stopPolling(){this.pollTimer&&(clearInterval(this.pollTimer),this.pollTimer=null)}_addListener(e,r){Object.keys(this.listeners).length===0&&(this.startPolling(),this.registerLifecycleListeners()),this.listeners[e]||(this.listeners[e]=new Set,this._get(e)),this.listeners[e].add(r)}_removeListener(e,r){this.listeners[e]&&(this.listeners[e].delete(r),this.listeners[e].size===0&&delete this.listeners[e]),Object.keys(this.listeners).length===0&&(this.stopPolling(),this.unregisterLifecycleListeners())}}tm.type="LOCAL";const Cy=tm;new Us(3e4,6e4);/**
 * @license
 * Copyright 2021 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */function Hu(i,e){return e?ar(e):(Ee(i._popupRedirectResolver,i,"argument-error"),i._popupRedirectResolver)}/**
 * @license
 * Copyright 2019 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */class Wu extends Bu{constructor(e){super("custom","custom"),this.params=e}_getIdTokenResponse(e){return Bi(e,this._buildIdpRequest())}_linkToIdToken(e,r){return Bi(e,this._buildIdpRequest(r))}_getReauthenticationResolver(e){return Bi(e,this._buildIdpRequest())}_buildIdpRequest(e){const r={requestUri:this.params.requestUri,sessionId:this.params.sessionId,postBody:this.params.postBody,tenantId:this.params.tenantId,pendingToken:this.params.pendingToken,returnSecureToken:!0,returnIdpCredential:!0};return e&&(r.idToken=e),r}}function Iy(i){return Wp(i.auth,new Wu(i),i.bypassAuthState)}function Ry(i){const{auth:e,user:r}=i;return Ee(r,e,"internal-error"),ty(r,new Wu(i),i.bypassAuthState)}async function Ny(i){const{auth:e,user:r}=i;return Ee(r,e,"internal-error"),ey(r,new Wu(i),i.bypassAuthState)}/**
 * @license
 * Copyright 2020 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */class nm{constructor(e,r,o,l,c=!1){this.auth=e,this.resolver=o,this.user=l,this.bypassAuthState=c,this.pendingPromise=null,this.eventManager=null,this.filter=Array.isArray(r)?r:[r]}execute(){return new Promise(async(e,r)=>{this.pendingPromise={resolve:e,reject:r};try{this.eventManager=await this.resolver._initialize(this.auth),await this.onExecution(),this.eventManager.registerConsumer(this)}catch(o){this.reject(o)}})}async onAuthEvent(e){const{urlResponse:r,sessionId:o,postBody:l,tenantId:c,error:h,type:m}=e;if(h){this.reject(h);return}const f={auth:this.auth,requestUri:r,sessionId:o,tenantId:c||void 0,postBody:l||void 0,user:this.user,bypassAuthState:this.bypassAuthState};try{this.resolve(await this.getIdpTask(m)(f))}catch(v){this.reject(v)}}onError(e){this.reject(e)}getIdpTask(e){switch(e){case"signInViaPopup":case"signInViaRedirect":return Iy;case"linkViaPopup":case"linkViaRedirect":return Ny;case"reauthViaPopup":case"reauthViaRedirect":return Ry;default:vn(this.auth,"internal-error")}}resolve(e){ur(this.pendingPromise,"Pending promise was never set"),this.pendingPromise.resolve(e),this.unregisterAndCleanUp()}reject(e){ur(this.pendingPromise,"Pending promise was never set"),this.pendingPromise.reject(e),this.unregisterAndCleanUp()}unregisterAndCleanUp(){this.eventManager&&this.eventManager.unregisterConsumer(this),this.pendingPromise=null,this.cleanUp()}}/**
 * @license
 * Copyright 2020 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */const Py=new Us(2e3,1e4);async function Ay(i,e,r){if(rn(i.app))return Promise.reject(Pn(i,"operation-not-supported-in-this-environment"));const o=Vn(i);Tp(i,e,ya);const l=Hu(o,r);return new ai(o,"signInViaPopup",e,l).executeNotNull()}class ai extends nm{constructor(e,r,o,l,c){super(e,r,l,c),this.provider=o,this.authWindow=null,this.pollId=null,ai.currentPopupAction&&ai.currentPopupAction.cancel(),ai.currentPopupAction=this}async executeNotNull(){const e=await this.execute();return Ee(e,this.auth,"internal-error"),e}async onExecution(){ur(this.filter.length===1,"Popup operations only handle one event");const e=Vu();this.authWindow=await this.resolver._openPopup(this.auth,this.provider,this.filter[0],e),this.authWindow.associatedEvent=e,this.resolver._originValidation(this.auth).catch(r=>{this.reject(r)}),this.resolver._isIframeWebStorageSupported(this.auth,r=>{r||this.reject(Pn(this.auth,"web-storage-unsupported"))}),this.pollUserCancellation()}get eventId(){var e;return((e=this.authWindow)==null?void 0:e.associatedEvent)||null}cancel(){this.reject(Pn(this.auth,"cancelled-popup-request"))}cleanUp(){this.authWindow&&this.authWindow.close(),this.pollId&&window.clearTimeout(this.pollId),this.authWindow=null,this.pollId=null,ai.currentPopupAction=null}pollUserCancellation(){const e=()=>{var r,o;if((o=(r=this.authWindow)==null?void 0:r.window)!=null&&o.closed){this.pollId=window.setTimeout(()=>{this.pollId=null,this.reject(Pn(this.auth,"popup-closed-by-user"))},8e3);return}this.pollId=window.setTimeout(e,Py.get())};e()}}ai.currentPopupAction=null;/**
 * @license
 * Copyright 2020 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */const My="pendingRedirect",sa=new Map;class Dy extends nm{constructor(e,r,o=!1){super(e,["signInViaRedirect","linkViaRedirect","reauthViaRedirect","unknown"],r,void 0,o),this.eventId=null}async execute(){let e=sa.get(this.auth._key());if(!e){try{const o=await by(this.resolver,this.auth)?await super.execute():null;e=()=>Promise.resolve(o)}catch(r){e=()=>Promise.reject(r)}sa.set(this.auth._key(),e)}return this.bypassAuthState||sa.set(this.auth._key(),()=>Promise.resolve(null)),e()}async onAuthEvent(e){if(e.type==="signInViaRedirect")return super.onAuthEvent(e);if(e.type==="unknown"){this.resolve(null);return}if(e.eventId){const r=await this.auth._redirectUserForId(e.eventId);if(r)return this.user=r,super.onAuthEvent(e);this.resolve(null)}}async onExecution(){}cleanUp(){}}async function by(i,e){const r=im(e),o=rm(i);if(!await o._isAvailable())return!1;const l=await o._get(r)==="true";return await o._remove(r),l}async function Ly(i,e){return rm(i)._set(im(e),"true")}function Oy(i,e){sa.set(i._key(),e)}function rm(i){return ar(i._redirectPersistence)}function im(i){return ia(My,i.config.apiKey,i.name)}/**
 * @license
 * Copyright 2020 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */function Fy(i,e,r){return zy(i,e,r)}async function zy(i,e,r){if(rn(i.app))return Promise.reject(jn(i));const o=Vn(i);Tp(i,e,ya),await o._initializationPromise;const l=Hu(o,r);return await Ly(l,o),l._openRedirect(o,e,"signInViaRedirect")}async function jy(i,e,r=!1){if(rn(i.app))return Promise.reject(jn(i));const o=Vn(i),l=Hu(o,e),h=await new Dy(o,l,r).execute();return h&&!r&&(delete h.user._redirectEventId,await o._persistUserIfCurrent(h.user),await o._setRedirectUser(null,e)),h}/**
 * @license
 * Copyright 2020 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */const Uy=600*1e3;class By{constructor(e){this.auth=e,this.cachedEventUids=new Set,this.consumers=new Set,this.queuedRedirectEvent=null,this.hasHandledPotentialRedirect=!1,this.lastProcessedEventTime=Date.now()}registerConsumer(e){this.consumers.add(e),this.queuedRedirectEvent&&this.isEventForConsumer(this.queuedRedirectEvent,e)&&(this.sendToConsumer(this.queuedRedirectEvent,e),this.saveEventToCache(this.queuedRedirectEvent),this.queuedRedirectEvent=null)}unregisterConsumer(e){this.consumers.delete(e)}onEvent(e){if(this.hasEventBeenHandled(e))return!1;let r=!1;return this.consumers.forEach(o=>{this.isEventForConsumer(e,o)&&(r=!0,this.sendToConsumer(e,o),this.saveEventToCache(e))}),this.hasHandledPotentialRedirect||!$y(e)||(this.hasHandledPotentialRedirect=!0,r||(this.queuedRedirectEvent=e,r=!0)),r}sendToConsumer(e,r){var o;if(e.error&&!sm(e)){const l=((o=e.error.code)==null?void 0:o.split("auth/")[1])||"internal-error";r.onError(Pn(this.auth,l))}else r.onAuthEvent(e)}isEventForConsumer(e,r){const o=r.eventId===null||!!e.eventId&&e.eventId===r.eventId;return r.filter.includes(e.type)&&o}hasEventBeenHandled(e){return Date.now()-this.lastProcessedEventTime>=Uy&&this.cachedEventUids.clear(),this.cachedEventUids.has(rf(e))}saveEventToCache(e){this.cachedEventUids.add(rf(e)),this.lastProcessedEventTime=Date.now()}}function rf(i){return[i.type,i.eventId,i.sessionId,i.tenantId].filter(e=>e).join("-")}function sm({type:i,error:e}){return i==="unknown"&&(e==null?void 0:e.code)==="auth/no-auth-event"}function $y(i){switch(i.type){case"signInViaRedirect":case"linkViaRedirect":case"reauthViaRedirect":return!0;case"unknown":return sm(i);default:return!1}}/**
 * @license
 * Copyright 2020 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */async function Vy(i,e={}){return $n(i,"GET","/v1/projects",e)}/**
 * @license
 * Copyright 2020 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */const Hy=/^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$/,Wy=/^https?/;async function Gy(i){if(i.config.emulator)return;const{authorizedDomains:e}=await Vy(i);for(const r of e)try{if(qy(r))return}catch{}vn(i,"unauthorized-domain")}function qy(i){const e=Ru(),{protocol:r,hostname:o}=new URL(e);if(i.startsWith("chrome-extension://")){const h=new URL(i);return h.hostname===""&&o===""?r==="chrome-extension:"&&i.replace("chrome-extension://","")===e.replace("chrome-extension://",""):r==="chrome-extension:"&&h.hostname===o}if(!Wy.test(r))return!1;if(Hy.test(i))return o===i;const l=i.replace(/\./g,"\\.");return new RegExp("^(.+\\."+l+"|"+l+")$","i").test(o)}/**
 * @license
 * Copyright 2020 Google LLC.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */const Ky=new Us(3e4,6e4);function sf(){const i=Un().___jsl;if(i!=null&&i.H){for(const e of Object.keys(i.H))if(i.H[e].r=i.H[e].r||[],i.H[e].L=i.H[e].L||[],i.H[e].r=[...i.H[e].L],i.CP)for(let r=0;r<i.CP.length;r++)i.CP[r]=null}}function Xy(i){return new Promise((e,r)=>{var l,c,h;function o(){sf(),gapi.load("gapi.iframes",{callback:()=>{e(gapi.iframes.getContext())},ontimeout:()=>{sf(),r(Pn(i,"network-request-failed"))},timeout:Ky.get()})}if((c=(l=Un().gapi)==null?void 0:l.iframes)!=null&&c.Iframe)e(gapi.iframes.getContext());else if((h=Un().gapi)!=null&&h.load)o();else{const m=L1("iframefcb");return Un()[m]=()=>{gapi.load?o():r(Pn(i,"network-request-failed"))},Bp(`${b1()}?onload=${m}`).catch(f=>r(f))}}).catch(e=>{throw oa=null,e})}let oa=null;function Yy(i){return oa=oa||Xy(i),oa}/**
 * @license
 * Copyright 2020 Google LLC.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */const Qy=new Us(5e3,15e3),Jy="__/auth/iframe",Zy="emulator/auth/iframe",ew={style:{position:"absolute",top:"-100px",width:"1px",height:"1px"},"aria-hidden":"true",tabindex:"-1"},tw=new Map([["identitytoolkit.googleapis.com","p"],["staging-identitytoolkit.sandbox.googleapis.com","s"],["test-identitytoolkit.sandbox.googleapis.com","t"]]);function nw(i){const e=i.config;Ee(e.authDomain,i,"auth-domain-config-required");const r=e.emulator?zu(e,Zy):`https://${i.config.authDomain}/${Jy}`,o={apiKey:e.apiKey,appName:i.name,v:js},l=tw.get(i.config.apiHost);l&&(o.eid=l);const c=i._getFrameworks();return c.length&&(o.fw=c.join(",")),`${r}?${zs(o).slice(1)}`}async function rw(i){const e=await Yy(i),r=Un().gapi;return Ee(r,i,"internal-error"),e.open({where:document.body,url:nw(i),messageHandlersFilter:r.iframes.CROSS_ORIGIN_IFRAMES_FILTER,attributes:ew,dontclear:!0},o=>new Promise(async(l,c)=>{await o.restyle({setHideOnLeave:!1});const h=Pn(i,"network-request-failed"),m=Un().setTimeout(()=>{c(h)},Qy.get());function f(){Un().clearTimeout(m),l(o)}o.ping(f).then(f,()=>{c(h)})}))}/**
 * @license
 * Copyright 2020 Google LLC.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */const iw={location:"yes",resizable:"yes",statusbar:"yes",toolbar:"no"},sw=500,ow=600,aw="_blank",lw="http://localhost";class of{constructor(e){this.window=e,this.associatedEvent=null}close(){if(this.window)try{this.window.close()}catch{}}}function uw(i,e,r,o=sw,l=ow){const c=Math.max((window.screen.availHeight-l)/2,0).toString(),h=Math.max((window.screen.availWidth-o)/2,0).toString();let m="";const f={...iw,width:o.toString(),height:l.toString(),top:c,left:h},v=Lt().toLowerCase();r&&(m=bp(v)?aw:r),Mp(v)&&(e=e||lw,f.scrollbars="yes");const x=Object.entries(f).reduce((T,[R,P])=>`${T}${R}=${P},`,"");if(T1(v)&&m!=="_self")return cw(e||"",m),new of(null);const S=window.open(e||"",m,x);Ee(S,i,"popup-blocked");try{S.focus()}catch{}return new of(S)}function cw(i,e){const r=document.createElement("a");r.href=i,r.target=e;const o=document.createEvent("MouseEvent");o.initMouseEvent("click",!0,!0,window,1,0,0,0,0,!1,!1,!1,!1,1,null),r.dispatchEvent(o)}/**
 * @license
 * Copyright 2021 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */const dw="__/auth/handler",hw="emulator/auth/handler",fw=encodeURIComponent("fac");async function af(i,e,r,o,l,c){Ee(i.config.authDomain,i,"auth-domain-config-required"),Ee(i.config.apiKey,i,"invalid-api-key");const h={apiKey:i.config.apiKey,appName:i.name,authType:r,redirectUrl:o,v:js,eventId:l};if(e instanceof ya){e.setDefaultLanguage(i.languageCode),h.providerId=e.providerId||"",W0(e.getCustomParameters())||(h.customParameters=JSON.stringify(e.getCustomParameters()));for(const[x,S]of Object.entries({}))h[x]=S}if(e instanceof $s){const x=e.getScopes().filter(S=>S!=="");x.length>0&&(h.scopes=x.join(","))}i.tenantId&&(h.tid=i.tenantId);const m=h;for(const x of Object.keys(m))m[x]===void 0&&delete m[x];const f=await i._getAppCheckToken(),v=f?`#${fw}=${encodeURIComponent(f)}`:"";return`${pw(i)}?${zs(m).slice(1)}${v}`}function pw({config:i}){return i.emulator?zu(i,hw):`https://${i.authDomain}/${dw}`}/**
 * @license
 * Copyright 2020 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */const fu="webStorageSupport";class mw{constructor(){this.eventManagers={},this.iframes={},this.originValidationPromises={},this._redirectPersistence=Yp,this._completeRedirectFn=jy,this._overrideRedirectResult=Oy}async _openPopup(e,r,o,l){var h;ur((h=this.eventManagers[e._key()])==null?void 0:h.manager,"_initialize() not called before _openPopup()");const c=await af(e,r,o,Ru(),l);return uw(e,c,Vu())}async _openRedirect(e,r,o,l){await this._originValidation(e);const c=await af(e,r,o,Ru(),l);return vy(c),new Promise(()=>{})}_initialize(e){const r=e._key();if(this.eventManagers[r]){const{manager:l,promise:c}=this.eventManagers[r];return l?Promise.resolve(l):(ur(c,"If manager is not set, promise should be"),c)}const o=this.initAndGetManager(e);return this.eventManagers[r]={promise:o},o.catch(()=>{delete this.eventManagers[r]}),o}async initAndGetManager(e){const r=await rw(e),o=new By(e);return r.register("authEvent",l=>(Ee(l==null?void 0:l.authEvent,e,"invalid-auth-event"),{status:o.onEvent(l.authEvent)?"ACK":"ERROR"}),gapi.iframes.CROSS_ORIGIN_IFRAMES_FILTER),this.eventManagers[e._key()]={manager:o},this.iframes[e._key()]=r,o}_isIframeWebStorageSupported(e,r){this.iframes[e._key()].send(fu,{type:fu},l=>{var h;const c=(h=l==null?void 0:l[0])==null?void 0:h[fu];c!==void 0&&r(!!c),vn(e,"internal-error")},gapi.iframes.CROSS_ORIGIN_IFRAMES_FILTER)}_originValidation(e){const r=e._key();return this.originValidationPromises[r]||(this.originValidationPromises[r]=Gy(e)),this.originValidationPromises[r]}get _shouldInitProactively(){return jp()||Dp()||Uu()}}const gw=mw;var lf="@firebase/auth",uf="1.13.8";/**
 * @license
 * Copyright 2020 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */class vw{constructor(e){this.auth=e,this.internalListeners=new Map}getUid(){var e;return this.assertAuthConfigured(),((e=this.auth.currentUser)==null?void 0:e.uid)||null}async getToken(e){return this.assertAuthConfigured(),await this.auth._initializationPromise,this.auth.currentUser?{accessToken:await this.auth.currentUser.getIdToken(e)}:null}addAuthTokenListener(e){if(this.assertAuthConfigured(),this.internalListeners.has(e))return;const r=this.auth.onIdTokenChanged(o=>{e((o==null?void 0:o.stsTokenManager.accessToken)||null)});this.internalListeners.set(e,r),this.updateProactiveRefresh()}removeAuthTokenListener(e){this.assertAuthConfigured();const r=this.internalListeners.get(e);r&&(this.internalListeners.delete(e),r(),this.updateProactiveRefresh())}assertAuthConfigured(){Ee(this.auth._initializationPromise,"dependent-sdk-initialized-before-auth")}updateProactiveRefresh(){this.internalListeners.size>0?this.auth._startProactiveRefresh():this.auth._stopProactiveRefresh()}}/**
 * @license
 * Copyright 2020 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */function yw(i){switch(i){case"Node":return"node";case"ReactNative":return"rn";case"Worker":return"webworker";case"Cordova":return"cordova";case"WebExtension":return"web-extension";default:return}}function ww(i){Ds(new Vi("auth",(e,{options:r})=>{const o=e.getProvider("app").getImmediate(),l=e.getProvider("heartbeat"),c=e.getProvider("app-check-internal"),{apiKey:h,authDomain:m}=o.options;Ee(h&&!h.includes(":"),"invalid-api-key",{appName:o.name});const f={apiKey:h,authDomain:m,clientPlatform:i,apiHost:"identitytoolkit.googleapis.com",tokenApiHost:"securetoken.googleapis.com",apiScheme:"https",sdkClientVersion:Up(i)},v=new A1(o,l,c,f);return U1(v,r),v},"PUBLIC").setInstantiationMode("EXPLICIT").setInstanceCreatedCallback((e,r,o)=>{e.getProvider("auth-internal").initialize()})),Ds(new Vi("auth-internal",e=>{const r=Vn(e.getProvider("auth").getImmediate());return(o=>new vw(o))(r)},"PRIVATE").setInstantiationMode("EXPLICIT")),ji(lf,uf,yw(i)),ji(lf,uf,"esm2020")}/**
 * @license
 * Copyright 2021 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */const xw=300,_w=fp("authIdTokenMaxAge")||xw;let cf=null;const Ew=i=>async e=>{const r=e&&await e.getIdTokenResult(),o=r&&(new Date().getTime()-Date.parse(r.issuedAtTime))/1e3;if(o&&o>_w)return;const l=r==null?void 0:r.token;cf!==l&&(cf=l,await fetch(i,{method:l?"POST":"DELETE",headers:l?{Authorization:`Bearer ${l}`}:{}}))};function Sw(i=xp()){const e=yp(i,"auth");if(e.isInitialized())return e.getImmediate();const r=j1(i,{popupRedirectResolver:gw,persistence:[Cy,py,Yp]}),o=fp("authTokenSyncURL");if(o&&typeof isSecureContext=="boolean"&&isSecureContext){const c=new URL(o,location.origin);if(location.origin===c.origin){const h=Ew(c.toString());uy(r,h,()=>h(r.currentUser)),ly(r,m=>h(m))}}const l=L0("auth");return l&&B1(r,`http://${l}`),r}function kw(){var i;return((i=document.getElementsByTagName("head"))==null?void 0:i[0])??document}M1({loadJS(i){return new Promise((e,r)=>{const o=document.createElement("script");o.setAttribute("src",i),o.onload=e,o.onerror=l=>{const c=Pn("internal-error");c.customData=l,r(c)},o.type="text/javascript",o.charset="UTF-8",kw().appendChild(o)})},gapiScript:"https://apis.google.com/js/api.js",recaptchaV2Script:"https://www.google.com/recaptcha/api.js",recaptchaEnterpriseScript:"https://www.google.com/recaptcha/enterprise.js?render="});ww("Browser");const Tw={apiKey:"AIzaSyMockKeyForDevelopmentModeOnly123456",authDomain:"nexora-ai.firebaseapp.com",projectId:"nexora-ai",storageBucket:"nexora-ai.appspot.com",messagingSenderId:"1234567890",appId:"1:1234567890:web:abcdef123456789"},Cw=Kv().length?xp():wp(Tw),si=Sw(Cw),Pu=new rr;Pu.setCustomParameters({prompt:"select_account"});const om=ne.createContext(null);function Iw({children:i}){const[e,r]=ne.useState(()=>{const x=localStorage.getItem("nexora_local_user");return x?JSON.parse(x):null}),[o,l]=ne.useState(!0);ne.useEffect(()=>{const x=cy(si,S=>{if(S){const T={uid:S.uid,email:S.email,displayName:S.displayName||S.email.split("@")[0],photoURL:S.photoURL};r(T),localStorage.setItem("nexora_local_user",JSON.stringify(T))}else localStorage.getItem("nexora_local_user")||r(null);l(!1)});return()=>x()},[]);const c=async(x,S)=>{try{const T=await sy(si,x,S),R={uid:T.user.uid,email:T.user.email,displayName:T.user.displayName||x.split("@")[0],photoURL:T.user.photoURL};return r(R),localStorage.setItem("nexora_local_user",JSON.stringify(R)),{success:!0,user:R}}catch(T){T.code==="auth/invalid-api-key"||T.code;{const R={uid:"demo-"+Date.now(),email:x,displayName:x.split("@")[0],photoURL:null};return r(R),localStorage.setItem("nexora_local_user",JSON.stringify(R)),{success:!0,user:R,demoMode:!0}}}},h=async(x,S,T)=>{try{const R=await iy(si,S,T);await ay(R.user,{displayName:x});const P={uid:R.user.uid,email:R.user.email,displayName:x,photoURL:R.user.photoURL};return r(P),localStorage.setItem("nexora_local_user",JSON.stringify(P)),{success:!0,user:P}}catch(R){R.code==="auth/invalid-api-key"||R.code;{const P={uid:"demo-"+Date.now(),email:S,displayName:x,photoURL:null};return r(P),localStorage.setItem("nexora_local_user",JSON.stringify(P)),{success:!0,user:P,demoMode:!0}}}},m=async()=>{try{if(/iPhone|iPad|iPod|Android/i.test(navigator.userAgent)){await Fy(si,Pu);return}const S=await Ay(si,Pu),T={uid:S.user.uid,email:S.user.email,displayName:S.user.displayName,photoURL:S.user.photoURL};return r(T),localStorage.setItem("nexora_local_user",JSON.stringify(T)),{success:!0,user:T}}catch(x){x.code==="auth/invalid-api-key"||x.code;{const S={uid:"google-demo-"+Date.now(),email:"google.user@example.com",displayName:"Demo Google User",photoURL:"https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=100&h=100&fit=crop&crop=faces"};return r(S),localStorage.setItem("nexora_local_user",JSON.stringify(S)),{success:!0,user:S,demoMode:!0}}}},f=async x=>{try{return await ry(si,x),{success:!0}}catch{return{success:!0,demoMode:!0}}},v=async()=>{try{await dy(si)}catch{}localStorage.removeItem("nexora_local_user"),r(null)};return g.jsx(om.Provider,{value:{user:e,loading:o,loginWithEmail:c,signupWithEmail:h,loginWithGoogle:m,resetPassword:f,signOut:v},children:i})}function am(){const i=ne.useContext(om);if(!i)throw new Error("useAuth must be used within an AuthProvider");return i}function As(i){let e=i[0],r=i[1],o=i[2];return Math.sqrt(e*e+r*r+o*o)}function Au(i,e){return i[0]=e[0],i[1]=e[1],i[2]=e[2],i}function Rw(i,e,r,o){return i[0]=e,i[1]=r,i[2]=o,i}function df(i,e,r){return i[0]=e[0]+r[0],i[1]=e[1]+r[1],i[2]=e[2]+r[2],i}function hf(i,e,r){return i[0]=e[0]-r[0],i[1]=e[1]-r[1],i[2]=e[2]-r[2],i}function Nw(i,e,r){return i[0]=e[0]*r[0],i[1]=e[1]*r[1],i[2]=e[2]*r[2],i}function Pw(i,e,r){return i[0]=e[0]/r[0],i[1]=e[1]/r[1],i[2]=e[2]/r[2],i}function pu(i,e,r){return i[0]=e[0]*r,i[1]=e[1]*r,i[2]=e[2]*r,i}function Aw(i,e){let r=e[0]-i[0],o=e[1]-i[1],l=e[2]-i[2];return Math.sqrt(r*r+o*o+l*l)}function Mw(i,e){let r=e[0]-i[0],o=e[1]-i[1],l=e[2]-i[2];return r*r+o*o+l*l}function ff(i){let e=i[0],r=i[1],o=i[2];return e*e+r*r+o*o}function Dw(i,e){return i[0]=-e[0],i[1]=-e[1],i[2]=-e[2],i}function bw(i,e){return i[0]=1/e[0],i[1]=1/e[1],i[2]=1/e[2],i}function Mu(i,e){let r=e[0],o=e[1],l=e[2],c=r*r+o*o+l*l;return c>0&&(c=1/Math.sqrt(c)),i[0]=e[0]*c,i[1]=e[1]*c,i[2]=e[2]*c,i}function lm(i,e){return i[0]*e[0]+i[1]*e[1]+i[2]*e[2]}function pf(i,e,r){let o=e[0],l=e[1],c=e[2],h=r[0],m=r[1],f=r[2];return i[0]=l*f-c*m,i[1]=c*h-o*f,i[2]=o*m-l*h,i}function Lw(i,e,r,o){let l=e[0],c=e[1],h=e[2];return i[0]=l+o*(r[0]-l),i[1]=c+o*(r[1]-c),i[2]=h+o*(r[2]-h),i}function Ow(i,e,r,o,l){const c=Math.exp(-o*l);let h=e[0],m=e[1],f=e[2];return i[0]=r[0]+(h-r[0])*c,i[1]=r[1]+(m-r[1])*c,i[2]=r[2]+(f-r[2])*c,i}function Fw(i,e,r){let o=e[0],l=e[1],c=e[2],h=r[3]*o+r[7]*l+r[11]*c+r[15];return h=h||1,i[0]=(r[0]*o+r[4]*l+r[8]*c+r[12])/h,i[1]=(r[1]*o+r[5]*l+r[9]*c+r[13])/h,i[2]=(r[2]*o+r[6]*l+r[10]*c+r[14])/h,i}function zw(i,e,r){let o=e[0],l=e[1],c=e[2],h=r[3]*o+r[7]*l+r[11]*c+r[15];return h=h||1,i[0]=(r[0]*o+r[4]*l+r[8]*c)/h,i[1]=(r[1]*o+r[5]*l+r[9]*c)/h,i[2]=(r[2]*o+r[6]*l+r[10]*c)/h,i}function jw(i,e,r){let o=e[0],l=e[1],c=e[2];return i[0]=o*r[0]+l*r[3]+c*r[6],i[1]=o*r[1]+l*r[4]+c*r[7],i[2]=o*r[2]+l*r[5]+c*r[8],i}function Uw(i,e,r){let o=e[0],l=e[1],c=e[2],h=r[0],m=r[1],f=r[2],v=r[3],x=m*c-f*l,S=f*o-h*c,T=h*l-m*o,R=m*T-f*S,P=f*x-h*T,b=h*S-m*x,A=v*2;return x*=A,S*=A,T*=A,R*=2,P*=2,b*=2,i[0]=o+x+R,i[1]=l+S+P,i[2]=c+T+b,i}const Bw=(function(){const i=[0,0,0],e=[0,0,0];return function(r,o){Au(i,r),Au(e,o),Mu(i,i),Mu(e,e);let l=lm(i,e);return l>1?0:l<-1?Math.PI:Math.acos(l)}})();function $w(i,e){return i[0]===e[0]&&i[1]===e[1]&&i[2]===e[2]}class Nn extends Array{constructor(e=0,r=e,o=e){return super(e,r,o),this}get x(){return this[0]}get y(){return this[1]}get z(){return this[2]}set x(e){this[0]=e}set y(e){this[1]=e}set z(e){this[2]=e}set(e,r=e,o=e){return e.length?this.copy(e):(Rw(this,e,r,o),this)}copy(e){return Au(this,e),this}add(e,r){return r?df(this,e,r):df(this,this,e),this}sub(e,r){return r?hf(this,e,r):hf(this,this,e),this}multiply(e){return e.length?Nw(this,this,e):pu(this,this,e),this}divide(e){return e.length?Pw(this,this,e):pu(this,this,1/e),this}inverse(e=this){return bw(this,e),this}len(){return As(this)}distance(e){return e?Aw(this,e):As(this)}squaredLen(){return ff(this)}squaredDistance(e){return e?Mw(this,e):ff(this)}negate(e=this){return Dw(this,e),this}cross(e,r){return r?pf(this,e,r):pf(this,this,e),this}scale(e){return pu(this,this,e),this}normalize(){return Mu(this,this),this}dot(e){return lm(this,e)}equals(e){return $w(this,e)}applyMatrix3(e){return jw(this,this,e),this}applyMatrix4(e){return Fw(this,this,e),this}scaleRotateMatrix4(e){return zw(this,this,e),this}applyQuaternion(e){return Uw(this,this,e),this}angle(e){return Bw(this,e)}lerp(e,r){return Lw(this,this,e,r),this}smoothLerp(e,r,o){return Ow(this,this,e,r,o),this}clone(){return new Nn(this[0],this[1],this[2])}fromArray(e,r=0){return this[0]=e[r],this[1]=e[r+1],this[2]=e[r+2],this}toArray(e=[],r=0){return e[r]=this[0],e[r+1]=this[1],e[r+2]=this[2],e}transformDirection(e){const r=this[0],o=this[1],l=this[2];return this[0]=e[0]*r+e[4]*o+e[8]*l,this[1]=e[1]*r+e[5]*o+e[9]*l,this[2]=e[2]*r+e[6]*o+e[10]*l,this.normalize()}}const mf=new Nn;let Vw=1,Hw=1,gf=!1;class um{constructor(e,r={}){e.canvas||console.error("gl not passed as first argument to Geometry"),this.gl=e,this.attributes=r,this.id=Vw++,this.VAOs={},this.drawRange={start:0,count:0},this.instancedCount=0,this.gl.renderer.bindVertexArray(null),this.gl.renderer.currentGeometry=null,this.glState=this.gl.renderer.state;for(let o in r)this.addAttribute(o,r[o])}addAttribute(e,r){if(this.attributes[e]=r,r.id=Hw++,r.size=r.size||1,r.type=r.type||(r.data.constructor===Float32Array?this.gl.FLOAT:r.data.constructor===Uint16Array?this.gl.UNSIGNED_SHORT:this.gl.UNSIGNED_INT),r.target=e==="index"?this.gl.ELEMENT_ARRAY_BUFFER:this.gl.ARRAY_BUFFER,r.normalized=r.normalized||!1,r.stride=r.stride||0,r.offset=r.offset||0,r.count=r.count||(r.stride?r.data.byteLength/r.stride:r.data.length/r.size),r.divisor=r.instanced||0,r.needsUpdate=!1,r.usage=r.usage||this.gl.STATIC_DRAW,r.buffer||this.updateAttribute(r),r.divisor){if(this.isInstanced=!0,this.instancedCount&&this.instancedCount!==r.count*r.divisor)return console.warn("geometry has multiple instanced buffers of different length"),this.instancedCount=Math.min(this.instancedCount,r.count*r.divisor);this.instancedCount=r.count*r.divisor}else e==="index"?this.drawRange.count=r.count:this.attributes.index||(this.drawRange.count=Math.max(this.drawRange.count,r.count))}updateAttribute(e){const r=!e.buffer;r&&(e.buffer=this.gl.createBuffer()),this.glState.boundBuffer!==e.buffer&&(this.gl.bindBuffer(e.target,e.buffer),this.glState.boundBuffer=e.buffer),r?this.gl.bufferData(e.target,e.data,e.usage):this.gl.bufferSubData(e.target,0,e.data),e.needsUpdate=!1}setIndex(e){this.addAttribute("index",e)}setDrawRange(e,r){this.drawRange.start=e,this.drawRange.count=r}setInstancedCount(e){this.instancedCount=e}createVAO(e){this.VAOs[e.attributeOrder]=this.gl.renderer.createVertexArray(),this.gl.renderer.bindVertexArray(this.VAOs[e.attributeOrder]),this.bindAttributes(e)}bindAttributes(e){e.attributeLocations.forEach((r,{name:o,type:l})=>{if(!this.attributes[o]){console.warn(`active attribute ${o} not being supplied`);return}const c=this.attributes[o];this.gl.bindBuffer(c.target,c.buffer),this.glState.boundBuffer=c.buffer;let h=1;l===35674&&(h=2),l===35675&&(h=3),l===35676&&(h=4);const m=c.size/h,f=h===1?0:h*h*4,v=h===1?0:h*4;for(let x=0;x<h;x++)this.gl.vertexAttribPointer(r+x,m,c.type,c.normalized,c.stride+f,c.offset+x*v),this.gl.enableVertexAttribArray(r+x),this.gl.renderer.vertexAttribDivisor(r+x,c.divisor)}),this.attributes.index&&this.gl.bindBuffer(this.gl.ELEMENT_ARRAY_BUFFER,this.attributes.index.buffer)}draw({program:e,mode:r=this.gl.TRIANGLES}){var l;this.gl.renderer.currentGeometry!==`${this.id}_${e.attributeOrder}`&&(this.VAOs[e.attributeOrder]||this.createVAO(e),this.gl.renderer.bindVertexArray(this.VAOs[e.attributeOrder]),this.gl.renderer.currentGeometry=`${this.id}_${e.attributeOrder}`),e.attributeLocations.forEach((c,{name:h})=>{const m=this.attributes[h];m.needsUpdate&&this.updateAttribute(m)});let o=2;((l=this.attributes.index)==null?void 0:l.type)===this.gl.UNSIGNED_INT&&(o=4),this.isInstanced?this.attributes.index?this.gl.renderer.drawElementsInstanced(r,this.drawRange.count,this.attributes.index.type,this.attributes.index.offset+this.drawRange.start*o,this.instancedCount):this.gl.renderer.drawArraysInstanced(r,this.drawRange.start,this.drawRange.count,this.instancedCount):this.attributes.index?this.gl.drawElements(r,this.drawRange.count,this.attributes.index.type,this.attributes.index.offset+this.drawRange.start*o):this.gl.drawArrays(r,this.drawRange.start,this.drawRange.count)}getPosition(){const e=this.attributes.position;if(e.data)return e;if(!gf)return console.warn("No position buffer data found to compute bounds"),gf=!0}computeBoundingBox(e){e||(e=this.getPosition());const r=e.data,o=e.size;this.bounds||(this.bounds={min:new Nn,max:new Nn,center:new Nn,scale:new Nn,radius:1/0});const l=this.bounds.min,c=this.bounds.max,h=this.bounds.center,m=this.bounds.scale;l.set(1/0),c.set(-1/0);for(let f=0,v=r.length;f<v;f+=o){const x=r[f],S=r[f+1],T=r[f+2];l.x=Math.min(x,l.x),l.y=Math.min(S,l.y),l.z=Math.min(T,l.z),c.x=Math.max(x,c.x),c.y=Math.max(S,c.y),c.z=Math.max(T,c.z)}m.sub(c,l),h.add(l,c).divide(2)}computeBoundingSphere(e){e||(e=this.getPosition());const r=e.data,o=e.size;this.bounds||this.computeBoundingBox(e);let l=0;for(let c=0,h=r.length;c<h;c+=o)mf.fromArray(r,c),l=Math.max(l,this.bounds.center.squaredDistance(mf));this.bounds.radius=Math.sqrt(l)}remove(){for(let e in this.VAOs)this.gl.renderer.deleteVertexArray(this.VAOs[e]),delete this.VAOs[e];for(let e in this.attributes)this.gl.deleteBuffer(this.attributes[e].buffer),delete this.attributes[e]}}let Ww=1;const vf={};class Jo{constructor(e,{vertex:r,fragment:o,uniforms:l={},transparent:c=!1,cullFace:h=e.BACK,frontFace:m=e.CCW,depthTest:f=!0,depthWrite:v=!0,depthFunc:x=e.LEQUAL}={}){e.canvas||console.error("gl not passed as first argument to Program"),this.gl=e,this.uniforms=l,this.id=Ww++,r||console.warn("vertex shader not supplied"),o||console.warn("fragment shader not supplied"),this.transparent=c,this.cullFace=h,this.frontFace=m,this.depthTest=f,this.depthWrite=v,this.depthFunc=x,this.blendFunc={},this.blendEquation={},this.stencilFunc={},this.stencilOp={},this.transparent&&!this.blendFunc.src&&(this.gl.renderer.premultipliedAlpha?this.setBlendFunc(this.gl.ONE,this.gl.ONE_MINUS_SRC_ALPHA):this.setBlendFunc(this.gl.SRC_ALPHA,this.gl.ONE_MINUS_SRC_ALPHA)),this.vertexShader=e.createShader(e.VERTEX_SHADER),this.fragmentShader=e.createShader(e.FRAGMENT_SHADER),this.program=e.createProgram(),e.attachShader(this.program,this.vertexShader),e.attachShader(this.program,this.fragmentShader),this.setShaders({vertex:r,fragment:o})}setShaders({vertex:e,fragment:r}){if(e&&(this.gl.shaderSource(this.vertexShader,e),this.gl.compileShader(this.vertexShader),this.gl.getShaderInfoLog(this.vertexShader)!==""&&console.warn(`${this.gl.getShaderInfoLog(this.vertexShader)}
Vertex Shader
${yf(e)}`)),r&&(this.gl.shaderSource(this.fragmentShader,r),this.gl.compileShader(this.fragmentShader),this.gl.getShaderInfoLog(this.fragmentShader)!==""&&console.warn(`${this.gl.getShaderInfoLog(this.fragmentShader)}
Fragment Shader
${yf(r)}`)),this.gl.linkProgram(this.program),!this.gl.getProgramParameter(this.program,this.gl.LINK_STATUS))return console.warn(this.gl.getProgramInfoLog(this.program));this.uniformLocations=new Map;let o=this.gl.getProgramParameter(this.program,this.gl.ACTIVE_UNIFORMS);for(let h=0;h<o;h++){let m=this.gl.getActiveUniform(this.program,h);this.uniformLocations.set(m,this.gl.getUniformLocation(this.program,m.name));const f=m.name.match(/(\w+)/g);m.uniformName=f[0],m.nameComponents=f.slice(1)}this.attributeLocations=new Map;const l=[],c=this.gl.getProgramParameter(this.program,this.gl.ACTIVE_ATTRIBUTES);for(let h=0;h<c;h++){const m=this.gl.getActiveAttrib(this.program,h),f=this.gl.getAttribLocation(this.program,m.name);f!==-1&&(l[f]=m.name,this.attributeLocations.set(m,f))}this.attributeOrder=l.join("")}setBlendFunc(e,r,o,l){this.blendFunc.src=e,this.blendFunc.dst=r,this.blendFunc.srcAlpha=o,this.blendFunc.dstAlpha=l,e&&(this.transparent=!0)}setBlendEquation(e,r){this.blendEquation.modeRGB=e,this.blendEquation.modeAlpha=r}setStencilFunc(e,r,o){this.stencilRef=r,this.stencilFunc.func=e,this.stencilFunc.ref=r,this.stencilFunc.mask=o}setStencilOp(e,r,o){this.stencilOp.stencilFail=e,this.stencilOp.depthFail=r,this.stencilOp.depthPass=o}applyState(){this.depthTest?this.gl.renderer.enable(this.gl.DEPTH_TEST):this.gl.renderer.disable(this.gl.DEPTH_TEST),this.cullFace?this.gl.renderer.enable(this.gl.CULL_FACE):this.gl.renderer.disable(this.gl.CULL_FACE),this.blendFunc.src?this.gl.renderer.enable(this.gl.BLEND):this.gl.renderer.disable(this.gl.BLEND),this.cullFace&&this.gl.renderer.setCullFace(this.cullFace),this.gl.renderer.setFrontFace(this.frontFace),this.gl.renderer.setDepthMask(this.depthWrite),this.gl.renderer.setDepthFunc(this.depthFunc),this.blendFunc.src&&this.gl.renderer.setBlendFunc(this.blendFunc.src,this.blendFunc.dst,this.blendFunc.srcAlpha,this.blendFunc.dstAlpha),this.gl.renderer.setBlendEquation(this.blendEquation.modeRGB,this.blendEquation.modeAlpha),this.stencilFunc.func||this.stencilOp.stencilFail?this.gl.renderer.enable(this.gl.STENCIL_TEST):this.gl.renderer.disable(this.gl.STENCIL_TEST),this.gl.renderer.setStencilFunc(this.stencilFunc.func,this.stencilFunc.ref,this.stencilFunc.mask),this.gl.renderer.setStencilOp(this.stencilOp.stencilFail,this.stencilOp.depthFail,this.stencilOp.depthPass)}use({flipFaces:e=!1}={}){let r=-1;this.gl.renderer.state.currentProgram===this.id||(this.gl.useProgram(this.program),this.gl.renderer.state.currentProgram=this.id),this.uniformLocations.forEach((l,c)=>{let h=this.uniforms[c.uniformName];for(const m of c.nameComponents){if(!h)break;if(m in h)h=h[m];else{if(Array.isArray(h.value))break;h=void 0;break}}if(!h)return wf(`Active uniform ${c.name} has not been supplied`);if(h&&h.value===void 0)return wf(`${c.name} uniform is missing a value parameter`);if(h.value.texture)return r=r+1,h.value.update(r),mu(this.gl,c.type,l,r);if(h.value.length&&h.value[0].texture){const m=[];return h.value.forEach(f=>{r=r+1,f.update(r),m.push(r)}),mu(this.gl,c.type,l,m)}mu(this.gl,c.type,l,h.value)}),this.applyState(),e&&this.gl.renderer.setFrontFace(this.frontFace===this.gl.CCW?this.gl.CW:this.gl.CCW)}remove(){this.gl.deleteProgram(this.program)}}function mu(i,e,r,o){o=o.length?Gw(o):o;const l=i.renderer.state.uniformLocations.get(r);if(o.length)if(l===void 0||l.length!==o.length)i.renderer.state.uniformLocations.set(r,o.slice(0));else{if(qw(l,o))return;l.set?l.set(o):Kw(l,o),i.renderer.state.uniformLocations.set(r,l)}else{if(l===o)return;i.renderer.state.uniformLocations.set(r,o)}switch(e){case 5126:return o.length?i.uniform1fv(r,o):i.uniform1f(r,o);case 35664:return i.uniform2fv(r,o);case 35665:return i.uniform3fv(r,o);case 35666:return i.uniform4fv(r,o);case 35670:case 5124:case 35678:case 36306:case 35680:case 36289:return o.length?i.uniform1iv(r,o):i.uniform1i(r,o);case 35671:case 35667:return i.uniform2iv(r,o);case 35672:case 35668:return i.uniform3iv(r,o);case 35673:case 35669:return i.uniform4iv(r,o);case 35674:return i.uniformMatrix2fv(r,!1,o);case 35675:return i.uniformMatrix3fv(r,!1,o);case 35676:return i.uniformMatrix4fv(r,!1,o)}}function yf(i){let e=i.split(`
`);for(let r=0;r<e.length;r++)e[r]=r+1+": "+e[r];return e.join(`
`)}function Gw(i){const e=i.length,r=i[0].length;if(r===void 0)return i;const o=e*r;let l=vf[o];l||(vf[o]=l=new Float32Array(o));for(let c=0;c<e;c++)l.set(i[c],c*r);return l}function qw(i,e){if(i.length!==e.length)return!1;for(let r=0,o=i.length;r<o;r++)if(i[r]!==e[r])return!1;return!0}function Kw(i,e){for(let r=0,o=i.length;r<o;r++)i[r]=e[r]}let gu=0;function wf(i){gu>100||(console.warn(i),gu++,gu>100&&console.warn("More than 100 program warnings - stopping logs."))}const vu=new Nn;let Xw=1;class Yw{constructor({canvas:e=document.createElement("canvas"),width:r=300,height:o=150,dpr:l=1,alpha:c=!1,depth:h=!0,stencil:m=!1,antialias:f=!1,premultipliedAlpha:v=!1,preserveDrawingBuffer:x=!1,powerPreference:S="default",autoClear:T=!0,webgl:R=2}={}){const P={alpha:c,depth:h,stencil:m,antialias:f,premultipliedAlpha:v,preserveDrawingBuffer:x,powerPreference:S};this.dpr=l,this.alpha=c,this.color=!0,this.depth=h,this.stencil=m,this.premultipliedAlpha=v,this.autoClear=T,this.id=Xw++,R===2&&(this.gl=e.getContext("webgl2",P)),this.isWebgl2=!!this.gl,this.gl||(this.gl=e.getContext("webgl",P)),this.gl||console.error("unable to create webgl context"),this.gl.renderer=this,this.setSize(r,o),this.state={},this.state.blendFunc={src:this.gl.ONE,dst:this.gl.ZERO},this.state.blendEquation={modeRGB:this.gl.FUNC_ADD},this.state.cullFace=!1,this.state.frontFace=this.gl.CCW,this.state.depthMask=!0,this.state.depthFunc=this.gl.LEQUAL,this.state.premultiplyAlpha=!1,this.state.flipY=!1,this.state.unpackAlignment=4,this.state.framebuffer=null,this.state.viewport={x:0,y:0,width:null,height:null},this.state.textureUnits=[],this.state.activeTextureUnit=0,this.state.boundBuffer=null,this.state.uniformLocations=new Map,this.state.currentProgram=null,this.extensions={},this.isWebgl2?(this.getExtension("EXT_color_buffer_float"),this.getExtension("OES_texture_float_linear")):(this.getExtension("OES_texture_float"),this.getExtension("OES_texture_float_linear"),this.getExtension("OES_texture_half_float"),this.getExtension("OES_texture_half_float_linear"),this.getExtension("OES_element_index_uint"),this.getExtension("OES_standard_derivatives"),this.getExtension("EXT_sRGB"),this.getExtension("WEBGL_depth_texture"),this.getExtension("WEBGL_draw_buffers")),this.getExtension("WEBGL_compressed_texture_astc"),this.getExtension("EXT_texture_compression_bptc"),this.getExtension("WEBGL_compressed_texture_s3tc"),this.getExtension("WEBGL_compressed_texture_etc1"),this.getExtension("WEBGL_compressed_texture_pvrtc"),this.getExtension("WEBKIT_WEBGL_compressed_texture_pvrtc"),this.vertexAttribDivisor=this.getExtension("ANGLE_instanced_arrays","vertexAttribDivisor","vertexAttribDivisorANGLE"),this.drawArraysInstanced=this.getExtension("ANGLE_instanced_arrays","drawArraysInstanced","drawArraysInstancedANGLE"),this.drawElementsInstanced=this.getExtension("ANGLE_instanced_arrays","drawElementsInstanced","drawElementsInstancedANGLE"),this.createVertexArray=this.getExtension("OES_vertex_array_object","createVertexArray","createVertexArrayOES"),this.bindVertexArray=this.getExtension("OES_vertex_array_object","bindVertexArray","bindVertexArrayOES"),this.deleteVertexArray=this.getExtension("OES_vertex_array_object","deleteVertexArray","deleteVertexArrayOES"),this.drawBuffers=this.getExtension("WEBGL_draw_buffers","drawBuffers","drawBuffersWEBGL"),this.parameters={},this.parameters.maxTextureUnits=this.gl.getParameter(this.gl.MAX_COMBINED_TEXTURE_IMAGE_UNITS),this.parameters.maxAnisotropy=this.getExtension("EXT_texture_filter_anisotropic")?this.gl.getParameter(this.getExtension("EXT_texture_filter_anisotropic").MAX_TEXTURE_MAX_ANISOTROPY_EXT):0}setSize(e,r){this.width=e,this.height=r,this.gl.canvas.width=e*this.dpr,this.gl.canvas.height=r*this.dpr,this.gl.canvas.style&&Object.assign(this.gl.canvas.style,{width:e+"px",height:r+"px"})}setViewport(e,r,o=0,l=0){this.state.viewport.width===e&&this.state.viewport.height===r||(this.state.viewport.width=e,this.state.viewport.height=r,this.state.viewport.x=o,this.state.viewport.y=l,this.gl.viewport(o,l,e,r))}setScissor(e,r,o=0,l=0){this.gl.scissor(o,l,e,r)}enable(e){this.state[e]!==!0&&(this.gl.enable(e),this.state[e]=!0)}disable(e){this.state[e]!==!1&&(this.gl.disable(e),this.state[e]=!1)}setBlendFunc(e,r,o,l){this.state.blendFunc.src===e&&this.state.blendFunc.dst===r&&this.state.blendFunc.srcAlpha===o&&this.state.blendFunc.dstAlpha===l||(this.state.blendFunc.src=e,this.state.blendFunc.dst=r,this.state.blendFunc.srcAlpha=o,this.state.blendFunc.dstAlpha=l,o!==void 0?this.gl.blendFuncSeparate(e,r,o,l):this.gl.blendFunc(e,r))}setBlendEquation(e,r){e=e||this.gl.FUNC_ADD,!(this.state.blendEquation.modeRGB===e&&this.state.blendEquation.modeAlpha===r)&&(this.state.blendEquation.modeRGB=e,this.state.blendEquation.modeAlpha=r,r!==void 0?this.gl.blendEquationSeparate(e,r):this.gl.blendEquation(e))}setCullFace(e){this.state.cullFace!==e&&(this.state.cullFace=e,this.gl.cullFace(e))}setFrontFace(e){this.state.frontFace!==e&&(this.state.frontFace=e,this.gl.frontFace(e))}setDepthMask(e){this.state.depthMask!==e&&(this.state.depthMask=e,this.gl.depthMask(e))}setDepthFunc(e){this.state.depthFunc!==e&&(this.state.depthFunc=e,this.gl.depthFunc(e))}setStencilMask(e){this.state.stencilMask!==e&&(this.state.stencilMask=e,this.gl.stencilMask(e))}setStencilFunc(e,r,o){this.state.stencilFunc===e&&this.state.stencilRef===r&&this.state.stencilFuncMask===o||(this.state.stencilFunc=e||this.gl.ALWAYS,this.state.stencilRef=r||0,this.state.stencilFuncMask=o||0,this.gl.stencilFunc(e||this.gl.ALWAYS,r||0,o||0))}setStencilOp(e,r,o){this.state.stencilFail===e&&this.state.stencilDepthFail===r&&this.state.stencilDepthPass===o||(this.state.stencilFail=e,this.state.stencilDepthFail=r,this.state.stencilDepthPass=o,this.gl.stencilOp(e,r,o))}activeTexture(e){this.state.activeTextureUnit!==e&&(this.state.activeTextureUnit=e,this.gl.activeTexture(this.gl.TEXTURE0+e))}bindFramebuffer({target:e=this.gl.FRAMEBUFFER,buffer:r=null}={}){this.state.framebuffer!==r&&(this.state.framebuffer=r,this.gl.bindFramebuffer(e,r))}getExtension(e,r,o){return r&&this.gl[r]?this.gl[r].bind(this.gl):(this.extensions[e]||(this.extensions[e]=this.gl.getExtension(e)),r?this.extensions[e]?this.extensions[e][o].bind(this.extensions[e]):null:this.extensions[e])}sortOpaque(e,r){return e.renderOrder!==r.renderOrder?e.renderOrder-r.renderOrder:e.program.id!==r.program.id?e.program.id-r.program.id:e.zDepth!==r.zDepth?e.zDepth-r.zDepth:r.id-e.id}sortTransparent(e,r){return e.renderOrder!==r.renderOrder?e.renderOrder-r.renderOrder:e.zDepth!==r.zDepth?r.zDepth-e.zDepth:r.id-e.id}sortUI(e,r){return e.renderOrder!==r.renderOrder?e.renderOrder-r.renderOrder:e.program.id!==r.program.id?e.program.id-r.program.id:r.id-e.id}getRenderList({scene:e,camera:r,frustumCull:o,sort:l}){let c=[];if(r&&o&&r.updateFrustum(),e.traverse(h=>{if(!h.visible)return!0;h.draw&&(o&&h.frustumCulled&&r&&!r.frustumIntersectsMesh(h)||c.push(h))}),l){const h=[],m=[],f=[];c.forEach(v=>{v.program.transparent?v.program.depthTest?m.push(v):f.push(v):h.push(v),v.zDepth=0,!(v.renderOrder!==0||!v.program.depthTest||!r)&&(v.worldMatrix.getTranslation(vu),vu.applyMatrix4(r.projectionViewMatrix),v.zDepth=vu.z)}),h.sort(this.sortOpaque),m.sort(this.sortTransparent),f.sort(this.sortUI),c=h.concat(m,f)}return c}render({scene:e,camera:r,target:o=null,update:l=!0,sort:c=!0,frustumCull:h=!0,clear:m}){o===null?(this.bindFramebuffer(),this.setViewport(this.width*this.dpr,this.height*this.dpr)):(this.bindFramebuffer(o),this.setViewport(o.width,o.height)),(m||this.autoClear&&m!==!1)&&(this.depth&&(!o||o.depth)&&(this.enable(this.gl.DEPTH_TEST),this.setDepthMask(!0)),(this.stencil||!o||o.stencil)&&(this.enable(this.gl.STENCIL_TEST),this.setStencilMask(255)),this.gl.clear((this.color?this.gl.COLOR_BUFFER_BIT:0)|(this.depth?this.gl.DEPTH_BUFFER_BIT:0)|(this.stencil?this.gl.STENCIL_BUFFER_BIT:0))),l&&e.updateMatrixWorld(),r&&r.updateMatrixWorld(),this.getRenderList({scene:e,camera:r,frustumCull:h,sort:c}).forEach(v=>{v.draw({camera:r})})}}function Qw(i,e){return i[0]=e[0],i[1]=e[1],i[2]=e[2],i[3]=e[3],i}function Jw(i,e,r,o,l){return i[0]=e,i[1]=r,i[2]=o,i[3]=l,i}function Zw(i,e){let r=e[0],o=e[1],l=e[2],c=e[3],h=r*r+o*o+l*l+c*c;return h>0&&(h=1/Math.sqrt(h)),i[0]=r*h,i[1]=o*h,i[2]=l*h,i[3]=c*h,i}function e2(i,e){return i[0]*e[0]+i[1]*e[1]+i[2]*e[2]+i[3]*e[3]}function t2(i){return i[0]=0,i[1]=0,i[2]=0,i[3]=1,i}function n2(i,e,r){r=r*.5;let o=Math.sin(r);return i[0]=o*e[0],i[1]=o*e[1],i[2]=o*e[2],i[3]=Math.cos(r),i}function xf(i,e,r){let o=e[0],l=e[1],c=e[2],h=e[3],m=r[0],f=r[1],v=r[2],x=r[3];return i[0]=o*x+h*m+l*v-c*f,i[1]=l*x+h*f+c*m-o*v,i[2]=c*x+h*v+o*f-l*m,i[3]=h*x-o*m-l*f-c*v,i}function r2(i,e,r){r*=.5;let o=e[0],l=e[1],c=e[2],h=e[3],m=Math.sin(r),f=Math.cos(r);return i[0]=o*f+h*m,i[1]=l*f+c*m,i[2]=c*f-l*m,i[3]=h*f-o*m,i}function i2(i,e,r){r*=.5;let o=e[0],l=e[1],c=e[2],h=e[3],m=Math.sin(r),f=Math.cos(r);return i[0]=o*f-c*m,i[1]=l*f+h*m,i[2]=c*f+o*m,i[3]=h*f-l*m,i}function s2(i,e,r){r*=.5;let o=e[0],l=e[1],c=e[2],h=e[3],m=Math.sin(r),f=Math.cos(r);return i[0]=o*f+l*m,i[1]=l*f-o*m,i[2]=c*f+h*m,i[3]=h*f-c*m,i}function o2(i,e,r,o){let l=e[0],c=e[1],h=e[2],m=e[3],f=r[0],v=r[1],x=r[2],S=r[3],T,R,P,b,A;return R=l*f+c*v+h*x+m*S,R<0&&(R=-R,f=-f,v=-v,x=-x,S=-S),1-R>1e-6?(T=Math.acos(R),P=Math.sin(T),b=Math.sin((1-o)*T)/P,A=Math.sin(o*T)/P):(b=1-o,A=o),i[0]=b*l+A*f,i[1]=b*c+A*v,i[2]=b*h+A*x,i[3]=b*m+A*S,i}function a2(i,e){let r=e[0],o=e[1],l=e[2],c=e[3],h=r*r+o*o+l*l+c*c,m=h?1/h:0;return i[0]=-r*m,i[1]=-o*m,i[2]=-l*m,i[3]=c*m,i}function l2(i,e){return i[0]=-e[0],i[1]=-e[1],i[2]=-e[2],i[3]=e[3],i}function u2(i,e){let r=e[0]+e[4]+e[8],o;if(r>0)o=Math.sqrt(r+1),i[3]=.5*o,o=.5/o,i[0]=(e[5]-e[7])*o,i[1]=(e[6]-e[2])*o,i[2]=(e[1]-e[3])*o;else{let l=0;e[4]>e[0]&&(l=1),e[8]>e[l*3+l]&&(l=2);let c=(l+1)%3,h=(l+2)%3;o=Math.sqrt(e[l*3+l]-e[c*3+c]-e[h*3+h]+1),i[l]=.5*o,o=.5/o,i[3]=(e[c*3+h]-e[h*3+c])*o,i[c]=(e[c*3+l]+e[l*3+c])*o,i[h]=(e[h*3+l]+e[l*3+h])*o}return i}function c2(i,e,r="YXZ"){let o=Math.sin(e[0]*.5),l=Math.cos(e[0]*.5),c=Math.sin(e[1]*.5),h=Math.cos(e[1]*.5),m=Math.sin(e[2]*.5),f=Math.cos(e[2]*.5);return r==="XYZ"?(i[0]=o*h*f+l*c*m,i[1]=l*c*f-o*h*m,i[2]=l*h*m+o*c*f,i[3]=l*h*f-o*c*m):r==="YXZ"?(i[0]=o*h*f+l*c*m,i[1]=l*c*f-o*h*m,i[2]=l*h*m-o*c*f,i[3]=l*h*f+o*c*m):r==="ZXY"?(i[0]=o*h*f-l*c*m,i[1]=l*c*f+o*h*m,i[2]=l*h*m+o*c*f,i[3]=l*h*f-o*c*m):r==="ZYX"?(i[0]=o*h*f-l*c*m,i[1]=l*c*f+o*h*m,i[2]=l*h*m-o*c*f,i[3]=l*h*f+o*c*m):r==="YZX"?(i[0]=o*h*f+l*c*m,i[1]=l*c*f+o*h*m,i[2]=l*h*m-o*c*f,i[3]=l*h*f-o*c*m):r==="XZY"&&(i[0]=o*h*f-l*c*m,i[1]=l*c*f-o*h*m,i[2]=l*h*m+o*c*f,i[3]=l*h*f+o*c*m),i}const d2=Qw,h2=Jw,f2=e2,p2=Zw;class m2 extends Array{constructor(e=0,r=0,o=0,l=1){super(e,r,o,l),this.onChange=()=>{},this._target=this;const c=["0","1","2","3"];return new Proxy(this,{set(h,m){const f=Reflect.set(...arguments);return f&&c.includes(m)&&h.onChange(),f}})}get x(){return this[0]}get y(){return this[1]}get z(){return this[2]}get w(){return this[3]}set x(e){this._target[0]=e,this.onChange()}set y(e){this._target[1]=e,this.onChange()}set z(e){this._target[2]=e,this.onChange()}set w(e){this._target[3]=e,this.onChange()}identity(){return t2(this._target),this.onChange(),this}set(e,r,o,l){return e.length?this.copy(e):(h2(this._target,e,r,o,l),this.onChange(),this)}rotateX(e){return r2(this._target,this._target,e),this.onChange(),this}rotateY(e){return i2(this._target,this._target,e),this.onChange(),this}rotateZ(e){return s2(this._target,this._target,e),this.onChange(),this}inverse(e=this._target){return a2(this._target,e),this.onChange(),this}conjugate(e=this._target){return l2(this._target,e),this.onChange(),this}copy(e){return d2(this._target,e),this.onChange(),this}normalize(e=this._target){return p2(this._target,e),this.onChange(),this}multiply(e,r){return r?xf(this._target,e,r):xf(this._target,this._target,e),this.onChange(),this}dot(e){return f2(this._target,e)}fromMatrix3(e){return u2(this._target,e),this.onChange(),this}fromEuler(e,r){return c2(this._target,e,e.order),r||this.onChange(),this}fromAxisAngle(e,r){return n2(this._target,e,r),this.onChange(),this}slerp(e,r){return o2(this._target,this._target,e,r),this.onChange(),this}fromArray(e,r=0){return this._target[0]=e[r],this._target[1]=e[r+1],this._target[2]=e[r+2],this._target[3]=e[r+3],this.onChange(),this}toArray(e=[],r=0){return e[r]=this[0],e[r+1]=this[1],e[r+2]=this[2],e[r+3]=this[3],e}}const g2=1e-6;function v2(i,e){return i[0]=e[0],i[1]=e[1],i[2]=e[2],i[3]=e[3],i[4]=e[4],i[5]=e[5],i[6]=e[6],i[7]=e[7],i[8]=e[8],i[9]=e[9],i[10]=e[10],i[11]=e[11],i[12]=e[12],i[13]=e[13],i[14]=e[14],i[15]=e[15],i}function y2(i,e,r,o,l,c,h,m,f,v,x,S,T,R,P,b,A){return i[0]=e,i[1]=r,i[2]=o,i[3]=l,i[4]=c,i[5]=h,i[6]=m,i[7]=f,i[8]=v,i[9]=x,i[10]=S,i[11]=T,i[12]=R,i[13]=P,i[14]=b,i[15]=A,i}function w2(i){return i[0]=1,i[1]=0,i[2]=0,i[3]=0,i[4]=0,i[5]=1,i[6]=0,i[7]=0,i[8]=0,i[9]=0,i[10]=1,i[11]=0,i[12]=0,i[13]=0,i[14]=0,i[15]=1,i}function x2(i,e){let r=e[0],o=e[1],l=e[2],c=e[3],h=e[4],m=e[5],f=e[6],v=e[7],x=e[8],S=e[9],T=e[10],R=e[11],P=e[12],b=e[13],A=e[14],F=e[15],se=r*m-o*h,q=r*f-l*h,B=r*v-c*h,W=o*f-l*m,Q=o*v-c*m,pe=l*v-c*f,de=x*b-S*P,w=x*A-T*P,Ne=x*F-R*P,we=S*A-T*b,ye=S*F-R*b,me=T*F-R*A,ue=se*me-q*ye+B*we+W*Ne-Q*w+pe*de;return ue?(ue=1/ue,i[0]=(m*me-f*ye+v*we)*ue,i[1]=(l*ye-o*me-c*we)*ue,i[2]=(b*pe-A*Q+F*W)*ue,i[3]=(T*Q-S*pe-R*W)*ue,i[4]=(f*Ne-h*me-v*w)*ue,i[5]=(r*me-l*Ne+c*w)*ue,i[6]=(A*B-P*pe-F*q)*ue,i[7]=(x*pe-T*B+R*q)*ue,i[8]=(h*ye-m*Ne+v*de)*ue,i[9]=(o*Ne-r*ye-c*de)*ue,i[10]=(P*Q-b*B+F*se)*ue,i[11]=(S*B-x*Q-R*se)*ue,i[12]=(m*w-h*we-f*de)*ue,i[13]=(r*we-o*w+l*de)*ue,i[14]=(b*q-P*W-A*se)*ue,i[15]=(x*W-S*q+T*se)*ue,i):null}function cm(i){let e=i[0],r=i[1],o=i[2],l=i[3],c=i[4],h=i[5],m=i[6],f=i[7],v=i[8],x=i[9],S=i[10],T=i[11],R=i[12],P=i[13],b=i[14],A=i[15],F=e*h-r*c,se=e*m-o*c,q=e*f-l*c,B=r*m-o*h,W=r*f-l*h,Q=o*f-l*m,pe=v*P-x*R,de=v*b-S*R,w=v*A-T*R,Ne=x*b-S*P,we=x*A-T*P,ye=S*A-T*b;return F*ye-se*we+q*Ne+B*w-W*de+Q*pe}function _f(i,e,r){let o=e[0],l=e[1],c=e[2],h=e[3],m=e[4],f=e[5],v=e[6],x=e[7],S=e[8],T=e[9],R=e[10],P=e[11],b=e[12],A=e[13],F=e[14],se=e[15],q=r[0],B=r[1],W=r[2],Q=r[3];return i[0]=q*o+B*m+W*S+Q*b,i[1]=q*l+B*f+W*T+Q*A,i[2]=q*c+B*v+W*R+Q*F,i[3]=q*h+B*x+W*P+Q*se,q=r[4],B=r[5],W=r[6],Q=r[7],i[4]=q*o+B*m+W*S+Q*b,i[5]=q*l+B*f+W*T+Q*A,i[6]=q*c+B*v+W*R+Q*F,i[7]=q*h+B*x+W*P+Q*se,q=r[8],B=r[9],W=r[10],Q=r[11],i[8]=q*o+B*m+W*S+Q*b,i[9]=q*l+B*f+W*T+Q*A,i[10]=q*c+B*v+W*R+Q*F,i[11]=q*h+B*x+W*P+Q*se,q=r[12],B=r[13],W=r[14],Q=r[15],i[12]=q*o+B*m+W*S+Q*b,i[13]=q*l+B*f+W*T+Q*A,i[14]=q*c+B*v+W*R+Q*F,i[15]=q*h+B*x+W*P+Q*se,i}function _2(i,e,r){let o=r[0],l=r[1],c=r[2],h,m,f,v,x,S,T,R,P,b,A,F;return e===i?(i[12]=e[0]*o+e[4]*l+e[8]*c+e[12],i[13]=e[1]*o+e[5]*l+e[9]*c+e[13],i[14]=e[2]*o+e[6]*l+e[10]*c+e[14],i[15]=e[3]*o+e[7]*l+e[11]*c+e[15]):(h=e[0],m=e[1],f=e[2],v=e[3],x=e[4],S=e[5],T=e[6],R=e[7],P=e[8],b=e[9],A=e[10],F=e[11],i[0]=h,i[1]=m,i[2]=f,i[3]=v,i[4]=x,i[5]=S,i[6]=T,i[7]=R,i[8]=P,i[9]=b,i[10]=A,i[11]=F,i[12]=h*o+x*l+P*c+e[12],i[13]=m*o+S*l+b*c+e[13],i[14]=f*o+T*l+A*c+e[14],i[15]=v*o+R*l+F*c+e[15]),i}function E2(i,e,r){let o=r[0],l=r[1],c=r[2];return i[0]=e[0]*o,i[1]=e[1]*o,i[2]=e[2]*o,i[3]=e[3]*o,i[4]=e[4]*l,i[5]=e[5]*l,i[6]=e[6]*l,i[7]=e[7]*l,i[8]=e[8]*c,i[9]=e[9]*c,i[10]=e[10]*c,i[11]=e[11]*c,i[12]=e[12],i[13]=e[13],i[14]=e[14],i[15]=e[15],i}function S2(i,e,r,o){let l=o[0],c=o[1],h=o[2],m=Math.hypot(l,c,h),f,v,x,S,T,R,P,b,A,F,se,q,B,W,Q,pe,de,w,Ne,we,ye,me,ue,Ve;return Math.abs(m)<g2?null:(m=1/m,l*=m,c*=m,h*=m,f=Math.sin(r),v=Math.cos(r),x=1-v,S=e[0],T=e[1],R=e[2],P=e[3],b=e[4],A=e[5],F=e[6],se=e[7],q=e[8],B=e[9],W=e[10],Q=e[11],pe=l*l*x+v,de=c*l*x+h*f,w=h*l*x-c*f,Ne=l*c*x-h*f,we=c*c*x+v,ye=h*c*x+l*f,me=l*h*x+c*f,ue=c*h*x-l*f,Ve=h*h*x+v,i[0]=S*pe+b*de+q*w,i[1]=T*pe+A*de+B*w,i[2]=R*pe+F*de+W*w,i[3]=P*pe+se*de+Q*w,i[4]=S*Ne+b*we+q*ye,i[5]=T*Ne+A*we+B*ye,i[6]=R*Ne+F*we+W*ye,i[7]=P*Ne+se*we+Q*ye,i[8]=S*me+b*ue+q*Ve,i[9]=T*me+A*ue+B*Ve,i[10]=R*me+F*ue+W*Ve,i[11]=P*me+se*ue+Q*Ve,e!==i&&(i[12]=e[12],i[13]=e[13],i[14]=e[14],i[15]=e[15]),i)}function k2(i,e){return i[0]=e[12],i[1]=e[13],i[2]=e[14],i}function dm(i,e){let r=e[0],o=e[1],l=e[2],c=e[4],h=e[5],m=e[6],f=e[8],v=e[9],x=e[10];return i[0]=Math.hypot(r,o,l),i[1]=Math.hypot(c,h,m),i[2]=Math.hypot(f,v,x),i}function T2(i){let e=i[0],r=i[1],o=i[2],l=i[4],c=i[5],h=i[6],m=i[8],f=i[9],v=i[10];const x=e*e+r*r+o*o,S=l*l+c*c+h*h,T=m*m+f*f+v*v;return Math.sqrt(Math.max(x,S,T))}const hm=(function(){const i=[1,1,1];return function(e,r){let o=i;dm(o,r);let l=1/o[0],c=1/o[1],h=1/o[2],m=r[0]*l,f=r[1]*c,v=r[2]*h,x=r[4]*l,S=r[5]*c,T=r[6]*h,R=r[8]*l,P=r[9]*c,b=r[10]*h,A=m+S+b,F=0;return A>0?(F=Math.sqrt(A+1)*2,e[3]=.25*F,e[0]=(T-P)/F,e[1]=(R-v)/F,e[2]=(f-x)/F):m>S&&m>b?(F=Math.sqrt(1+m-S-b)*2,e[3]=(T-P)/F,e[0]=.25*F,e[1]=(f+x)/F,e[2]=(R+v)/F):S>b?(F=Math.sqrt(1+S-m-b)*2,e[3]=(R-v)/F,e[0]=(f+x)/F,e[1]=.25*F,e[2]=(T+P)/F):(F=Math.sqrt(1+b-m-S)*2,e[3]=(f-x)/F,e[0]=(R+v)/F,e[1]=(T+P)/F,e[2]=.25*F),e}})();function C2(i,e,r,o){let l=As([i[0],i[1],i[2]]);const c=As([i[4],i[5],i[6]]),h=As([i[8],i[9],i[10]]);cm(i)<0&&(l=-l),r[0]=i[12],r[1]=i[13],r[2]=i[14];const f=i.slice(),v=1/l,x=1/c,S=1/h;f[0]*=v,f[1]*=v,f[2]*=v,f[4]*=x,f[5]*=x,f[6]*=x,f[8]*=S,f[9]*=S,f[10]*=S,hm(e,f),o[0]=l,o[1]=c,o[2]=h}function I2(i,e,r,o){const l=i,c=e[0],h=e[1],m=e[2],f=e[3],v=c+c,x=h+h,S=m+m,T=c*v,R=c*x,P=c*S,b=h*x,A=h*S,F=m*S,se=f*v,q=f*x,B=f*S,W=o[0],Q=o[1],pe=o[2];return l[0]=(1-(b+F))*W,l[1]=(R+B)*W,l[2]=(P-q)*W,l[3]=0,l[4]=(R-B)*Q,l[5]=(1-(T+F))*Q,l[6]=(A+se)*Q,l[7]=0,l[8]=(P+q)*pe,l[9]=(A-se)*pe,l[10]=(1-(T+b))*pe,l[11]=0,l[12]=r[0],l[13]=r[1],l[14]=r[2],l[15]=1,l}function R2(i,e){let r=e[0],o=e[1],l=e[2],c=e[3],h=r+r,m=o+o,f=l+l,v=r*h,x=o*h,S=o*m,T=l*h,R=l*m,P=l*f,b=c*h,A=c*m,F=c*f;return i[0]=1-S-P,i[1]=x+F,i[2]=T-A,i[3]=0,i[4]=x-F,i[5]=1-v-P,i[6]=R+b,i[7]=0,i[8]=T+A,i[9]=R-b,i[10]=1-v-S,i[11]=0,i[12]=0,i[13]=0,i[14]=0,i[15]=1,i}function N2(i,e,r,o,l){let c=1/Math.tan(e/2),h=1/(o-l);return i[0]=c/r,i[1]=0,i[2]=0,i[3]=0,i[4]=0,i[5]=c,i[6]=0,i[7]=0,i[8]=0,i[9]=0,i[10]=(l+o)*h,i[11]=-1,i[12]=0,i[13]=0,i[14]=2*l*o*h,i[15]=0,i}function P2(i,e,r,o,l,c,h){let m=1/(e-r),f=1/(o-l),v=1/(c-h);return i[0]=-2*m,i[1]=0,i[2]=0,i[3]=0,i[4]=0,i[5]=-2*f,i[6]=0,i[7]=0,i[8]=0,i[9]=0,i[10]=2*v,i[11]=0,i[12]=(e+r)*m,i[13]=(l+o)*f,i[14]=(h+c)*v,i[15]=1,i}function A2(i,e,r,o){let l=e[0],c=e[1],h=e[2],m=o[0],f=o[1],v=o[2],x=l-r[0],S=c-r[1],T=h-r[2],R=x*x+S*S+T*T;R===0?T=1:(R=1/Math.sqrt(R),x*=R,S*=R,T*=R);let P=f*T-v*S,b=v*x-m*T,A=m*S-f*x;return R=P*P+b*b+A*A,R===0&&(v?m+=1e-6:f?v+=1e-6:f+=1e-6,P=f*T-v*S,b=v*x-m*T,A=m*S-f*x,R=P*P+b*b+A*A),R=1/Math.sqrt(R),P*=R,b*=R,A*=R,i[0]=P,i[1]=b,i[2]=A,i[3]=0,i[4]=S*A-T*b,i[5]=T*P-x*A,i[6]=x*b-S*P,i[7]=0,i[8]=x,i[9]=S,i[10]=T,i[11]=0,i[12]=l,i[13]=c,i[14]=h,i[15]=1,i}function Ef(i,e,r){return i[0]=e[0]+r[0],i[1]=e[1]+r[1],i[2]=e[2]+r[2],i[3]=e[3]+r[3],i[4]=e[4]+r[4],i[5]=e[5]+r[5],i[6]=e[6]+r[6],i[7]=e[7]+r[7],i[8]=e[8]+r[8],i[9]=e[9]+r[9],i[10]=e[10]+r[10],i[11]=e[11]+r[11],i[12]=e[12]+r[12],i[13]=e[13]+r[13],i[14]=e[14]+r[14],i[15]=e[15]+r[15],i}function Sf(i,e,r){return i[0]=e[0]-r[0],i[1]=e[1]-r[1],i[2]=e[2]-r[2],i[3]=e[3]-r[3],i[4]=e[4]-r[4],i[5]=e[5]-r[5],i[6]=e[6]-r[6],i[7]=e[7]-r[7],i[8]=e[8]-r[8],i[9]=e[9]-r[9],i[10]=e[10]-r[10],i[11]=e[11]-r[11],i[12]=e[12]-r[12],i[13]=e[13]-r[13],i[14]=e[14]-r[14],i[15]=e[15]-r[15],i}function M2(i,e,r){return i[0]=e[0]*r,i[1]=e[1]*r,i[2]=e[2]*r,i[3]=e[3]*r,i[4]=e[4]*r,i[5]=e[5]*r,i[6]=e[6]*r,i[7]=e[7]*r,i[8]=e[8]*r,i[9]=e[9]*r,i[10]=e[10]*r,i[11]=e[11]*r,i[12]=e[12]*r,i[13]=e[13]*r,i[14]=e[14]*r,i[15]=e[15]*r,i}class pa extends Array{constructor(e=1,r=0,o=0,l=0,c=0,h=1,m=0,f=0,v=0,x=0,S=1,T=0,R=0,P=0,b=0,A=1){return super(e,r,o,l,c,h,m,f,v,x,S,T,R,P,b,A),this}get x(){return this[12]}get y(){return this[13]}get z(){return this[14]}get w(){return this[15]}set x(e){this[12]=e}set y(e){this[13]=e}set z(e){this[14]=e}set w(e){this[15]=e}set(e,r,o,l,c,h,m,f,v,x,S,T,R,P,b,A){return e.length?this.copy(e):(y2(this,e,r,o,l,c,h,m,f,v,x,S,T,R,P,b,A),this)}translate(e,r=this){return _2(this,r,e),this}rotate(e,r,o=this){return S2(this,o,e,r),this}scale(e,r=this){return E2(this,r,typeof e=="number"?[e,e,e]:e),this}add(e,r){return r?Ef(this,e,r):Ef(this,this,e),this}sub(e,r){return r?Sf(this,e,r):Sf(this,this,e),this}multiply(e,r){return e.length?r?_f(this,e,r):_f(this,this,e):M2(this,this,e),this}identity(){return w2(this),this}copy(e){return v2(this,e),this}fromPerspective({fov:e,aspect:r,near:o,far:l}={}){return N2(this,e,r,o,l),this}fromOrthogonal({left:e,right:r,bottom:o,top:l,near:c,far:h}){return P2(this,e,r,o,l,c,h),this}fromQuaternion(e){return R2(this,e),this}setPosition(e){return this.x=e[0],this.y=e[1],this.z=e[2],this}inverse(e=this){return x2(this,e),this}compose(e,r,o){return I2(this,e,r,o),this}decompose(e,r,o){return C2(this,e,r,o),this}getRotation(e){return hm(e,this),this}getTranslation(e){return k2(e,this),this}getScaling(e){return dm(e,this),this}getMaxScaleOnAxis(){return T2(this)}lookAt(e,r,o){return A2(this,e,r,o),this}determinant(){return cm(this)}fromArray(e,r=0){return this[0]=e[r],this[1]=e[r+1],this[2]=e[r+2],this[3]=e[r+3],this[4]=e[r+4],this[5]=e[r+5],this[6]=e[r+6],this[7]=e[r+7],this[8]=e[r+8],this[9]=e[r+9],this[10]=e[r+10],this[11]=e[r+11],this[12]=e[r+12],this[13]=e[r+13],this[14]=e[r+14],this[15]=e[r+15],this}toArray(e=[],r=0){return e[r]=this[0],e[r+1]=this[1],e[r+2]=this[2],e[r+3]=this[3],e[r+4]=this[4],e[r+5]=this[5],e[r+6]=this[6],e[r+7]=this[7],e[r+8]=this[8],e[r+9]=this[9],e[r+10]=this[10],e[r+11]=this[11],e[r+12]=this[12],e[r+13]=this[13],e[r+14]=this[14],e[r+15]=this[15],e}}function D2(i,e,r="YXZ"){return r==="XYZ"?(i[1]=Math.asin(Math.min(Math.max(e[8],-1),1)),Math.abs(e[8])<.99999?(i[0]=Math.atan2(-e[9],e[10]),i[2]=Math.atan2(-e[4],e[0])):(i[0]=Math.atan2(e[6],e[5]),i[2]=0)):r==="YXZ"?(i[0]=Math.asin(-Math.min(Math.max(e[9],-1),1)),Math.abs(e[9])<.99999?(i[1]=Math.atan2(e[8],e[10]),i[2]=Math.atan2(e[1],e[5])):(i[1]=Math.atan2(-e[2],e[0]),i[2]=0)):r==="ZXY"?(i[0]=Math.asin(Math.min(Math.max(e[6],-1),1)),Math.abs(e[6])<.99999?(i[1]=Math.atan2(-e[2],e[10]),i[2]=Math.atan2(-e[4],e[5])):(i[1]=0,i[2]=Math.atan2(e[1],e[0]))):r==="ZYX"?(i[1]=Math.asin(-Math.min(Math.max(e[2],-1),1)),Math.abs(e[2])<.99999?(i[0]=Math.atan2(e[6],e[10]),i[2]=Math.atan2(e[1],e[0])):(i[0]=0,i[2]=Math.atan2(-e[4],e[5]))):r==="YZX"?(i[2]=Math.asin(Math.min(Math.max(e[1],-1),1)),Math.abs(e[1])<.99999?(i[0]=Math.atan2(-e[9],e[5]),i[1]=Math.atan2(-e[2],e[0])):(i[0]=0,i[1]=Math.atan2(e[8],e[10]))):r==="XZY"&&(i[2]=Math.asin(-Math.min(Math.max(e[4],-1),1)),Math.abs(e[4])<.99999?(i[0]=Math.atan2(e[6],e[5]),i[1]=Math.atan2(e[8],e[0])):(i[0]=Math.atan2(-e[9],e[10]),i[1]=0)),i}const kf=new pa;class b2 extends Array{constructor(e=0,r=e,o=e,l="YXZ"){super(e,r,o),this.order=l,this.onChange=()=>{},this._target=this;const c=["0","1","2"];return new Proxy(this,{set(h,m){const f=Reflect.set(...arguments);return f&&c.includes(m)&&h.onChange(),f}})}get x(){return this[0]}get y(){return this[1]}get z(){return this[2]}set x(e){this._target[0]=e,this.onChange()}set y(e){this._target[1]=e,this.onChange()}set z(e){this._target[2]=e,this.onChange()}set(e,r=e,o=e){return e.length?this.copy(e):(this._target[0]=e,this._target[1]=r,this._target[2]=o,this.onChange(),this)}copy(e){return this._target[0]=e[0],this._target[1]=e[1],this._target[2]=e[2],this.onChange(),this}reorder(e){return this._target.order=e,this.onChange(),this}fromRotationMatrix(e,r=this.order){return D2(this._target,e,r),this.onChange(),this}fromQuaternion(e,r=this.order,o){return kf.fromQuaternion(e),this._target.fromRotationMatrix(kf,r),o||this.onChange(),this}fromArray(e,r=0){return this._target[0]=e[r],this._target[1]=e[r+1],this._target[2]=e[r+2],this}toArray(e=[],r=0){return e[r]=this[0],e[r+1]=this[1],e[r+2]=this[2],e}}class L2{constructor(){this.parent=null,this.children=[],this.visible=!0,this.matrix=new pa,this.worldMatrix=new pa,this.matrixAutoUpdate=!0,this.worldMatrixNeedsUpdate=!1,this.position=new Nn,this.quaternion=new m2,this.scale=new Nn(1),this.rotation=new b2,this.up=new Nn(0,1,0),this.rotation._target.onChange=()=>this.quaternion.fromEuler(this.rotation,!0),this.quaternion._target.onChange=()=>this.rotation.fromQuaternion(this.quaternion,void 0,!0)}setParent(e,r=!0){this.parent&&e!==this.parent&&this.parent.removeChild(this,!1),this.parent=e,r&&e&&e.addChild(this,!1)}addChild(e,r=!0){~this.children.indexOf(e)||this.children.push(e),r&&e.setParent(this,!1)}removeChild(e,r=!0){~this.children.indexOf(e)&&this.children.splice(this.children.indexOf(e),1),r&&e.setParent(null,!1)}updateMatrixWorld(e){this.matrixAutoUpdate&&this.updateMatrix(),(this.worldMatrixNeedsUpdate||e)&&(this.parent===null?this.worldMatrix.copy(this.matrix):this.worldMatrix.multiply(this.parent.worldMatrix,this.matrix),this.worldMatrixNeedsUpdate=!1,e=!0);for(let r=0,o=this.children.length;r<o;r++)this.children[r].updateMatrixWorld(e)}updateMatrix(){this.matrix.compose(this.quaternion,this.position,this.scale),this.worldMatrixNeedsUpdate=!0}traverse(e){if(!e(this))for(let r=0,o=this.children.length;r<o;r++)this.children[r].traverse(e)}decompose(){this.matrix.decompose(this.quaternion._target,this.position,this.scale),this.rotation.fromQuaternion(this.quaternion)}lookAt(e,r=!1){r?this.matrix.lookAt(this.position,e,this.up):this.matrix.lookAt(e,this.position,this.up),this.matrix.getRotation(this.quaternion._target),this.rotation.fromQuaternion(this.quaternion)}}function O2(i,e){return i[0]=e[0],i[1]=e[1],i[2]=e[2],i[3]=e[4],i[4]=e[5],i[5]=e[6],i[6]=e[8],i[7]=e[9],i[8]=e[10],i}function F2(i,e){let r=e[0],o=e[1],l=e[2],c=e[3],h=r+r,m=o+o,f=l+l,v=r*h,x=o*h,S=o*m,T=l*h,R=l*m,P=l*f,b=c*h,A=c*m,F=c*f;return i[0]=1-S-P,i[3]=x-F,i[6]=T+A,i[1]=x+F,i[4]=1-v-P,i[7]=R-b,i[2]=T-A,i[5]=R+b,i[8]=1-v-S,i}function z2(i,e){return i[0]=e[0],i[1]=e[1],i[2]=e[2],i[3]=e[3],i[4]=e[4],i[5]=e[5],i[6]=e[6],i[7]=e[7],i[8]=e[8],i}function j2(i,e,r,o,l,c,h,m,f,v){return i[0]=e,i[1]=r,i[2]=o,i[3]=l,i[4]=c,i[5]=h,i[6]=m,i[7]=f,i[8]=v,i}function U2(i){return i[0]=1,i[1]=0,i[2]=0,i[3]=0,i[4]=1,i[5]=0,i[6]=0,i[7]=0,i[8]=1,i}function B2(i,e){let r=e[0],o=e[1],l=e[2],c=e[3],h=e[4],m=e[5],f=e[6],v=e[7],x=e[8],S=x*h-m*v,T=-x*c+m*f,R=v*c-h*f,P=r*S+o*T+l*R;return P?(P=1/P,i[0]=S*P,i[1]=(-x*o+l*v)*P,i[2]=(m*o-l*h)*P,i[3]=T*P,i[4]=(x*r-l*f)*P,i[5]=(-m*r+l*c)*P,i[6]=R*P,i[7]=(-v*r+o*f)*P,i[8]=(h*r-o*c)*P,i):null}function Tf(i,e,r){let o=e[0],l=e[1],c=e[2],h=e[3],m=e[4],f=e[5],v=e[6],x=e[7],S=e[8],T=r[0],R=r[1],P=r[2],b=r[3],A=r[4],F=r[5],se=r[6],q=r[7],B=r[8];return i[0]=T*o+R*h+P*v,i[1]=T*l+R*m+P*x,i[2]=T*c+R*f+P*S,i[3]=b*o+A*h+F*v,i[4]=b*l+A*m+F*x,i[5]=b*c+A*f+F*S,i[6]=se*o+q*h+B*v,i[7]=se*l+q*m+B*x,i[8]=se*c+q*f+B*S,i}function $2(i,e,r){let o=e[0],l=e[1],c=e[2],h=e[3],m=e[4],f=e[5],v=e[6],x=e[7],S=e[8],T=r[0],R=r[1];return i[0]=o,i[1]=l,i[2]=c,i[3]=h,i[4]=m,i[5]=f,i[6]=T*o+R*h+v,i[7]=T*l+R*m+x,i[8]=T*c+R*f+S,i}function V2(i,e,r){let o=e[0],l=e[1],c=e[2],h=e[3],m=e[4],f=e[5],v=e[6],x=e[7],S=e[8],T=Math.sin(r),R=Math.cos(r);return i[0]=R*o+T*h,i[1]=R*l+T*m,i[2]=R*c+T*f,i[3]=R*h-T*o,i[4]=R*m-T*l,i[5]=R*f-T*c,i[6]=v,i[7]=x,i[8]=S,i}function H2(i,e,r){let o=r[0],l=r[1];return i[0]=o*e[0],i[1]=o*e[1],i[2]=o*e[2],i[3]=l*e[3],i[4]=l*e[4],i[5]=l*e[5],i[6]=e[6],i[7]=e[7],i[8]=e[8],i}function W2(i,e){let r=e[0],o=e[1],l=e[2],c=e[3],h=e[4],m=e[5],f=e[6],v=e[7],x=e[8],S=e[9],T=e[10],R=e[11],P=e[12],b=e[13],A=e[14],F=e[15],se=r*m-o*h,q=r*f-l*h,B=r*v-c*h,W=o*f-l*m,Q=o*v-c*m,pe=l*v-c*f,de=x*b-S*P,w=x*A-T*P,Ne=x*F-R*P,we=S*A-T*b,ye=S*F-R*b,me=T*F-R*A,ue=se*me-q*ye+B*we+W*Ne-Q*w+pe*de;return ue?(ue=1/ue,i[0]=(m*me-f*ye+v*we)*ue,i[1]=(f*Ne-h*me-v*w)*ue,i[2]=(h*ye-m*Ne+v*de)*ue,i[3]=(l*ye-o*me-c*we)*ue,i[4]=(r*me-l*Ne+c*w)*ue,i[5]=(o*Ne-r*ye-c*de)*ue,i[6]=(b*pe-A*Q+F*W)*ue,i[7]=(A*B-P*pe-F*q)*ue,i[8]=(P*Q-b*B+F*se)*ue,i):null}class G2 extends Array{constructor(e=1,r=0,o=0,l=0,c=1,h=0,m=0,f=0,v=1){return super(e,r,o,l,c,h,m,f,v),this}set(e,r,o,l,c,h,m,f,v){return e.length?this.copy(e):(j2(this,e,r,o,l,c,h,m,f,v),this)}translate(e,r=this){return $2(this,r,e),this}rotate(e,r=this){return V2(this,r,e),this}scale(e,r=this){return H2(this,r,e),this}multiply(e,r){return r?Tf(this,e,r):Tf(this,this,e),this}identity(){return U2(this),this}copy(e){return z2(this,e),this}fromMatrix4(e){return O2(this,e),this}fromQuaternion(e){return F2(this,e),this}fromBasis(e,r,o){return this.set(e[0],e[1],e[2],r[0],r[1],r[2],o[0],o[1],o[2]),this}inverse(e=this){return B2(this,e),this}getNormalMatrix(e){return W2(this,e),this}}let q2=0;class Zo extends L2{constructor(e,{geometry:r,program:o,mode:l=e.TRIANGLES,frustumCulled:c=!0,renderOrder:h=0}={}){super(),e.canvas||console.error("gl not passed as first argument to Mesh"),this.gl=e,this.id=q2++,this.geometry=r,this.program=o,this.mode=l,this.frustumCulled=c,this.renderOrder=h,this.modelViewMatrix=new pa,this.normalMatrix=new G2,this.beforeRenderCallbacks=[],this.afterRenderCallbacks=[]}onBeforeRender(e){return this.beforeRenderCallbacks.push(e),this}onAfterRender(e){return this.afterRenderCallbacks.push(e),this}draw({camera:e}={}){e&&(this.program.uniforms.modelMatrix||Object.assign(this.program.uniforms,{modelMatrix:{value:null},viewMatrix:{value:null},modelViewMatrix:{value:null},normalMatrix:{value:null},projectionMatrix:{value:null},cameraPosition:{value:null}}),this.program.uniforms.projectionMatrix.value=e.projectionMatrix,this.program.uniforms.cameraPosition.value=e.worldPosition,this.program.uniforms.viewMatrix.value=e.viewMatrix,this.modelViewMatrix.multiply(e.viewMatrix,this.worldMatrix),this.normalMatrix.getNormalMatrix(this.modelViewMatrix),this.program.uniforms.modelMatrix.value=this.worldMatrix,this.program.uniforms.modelViewMatrix.value=this.modelViewMatrix,this.program.uniforms.normalMatrix.value=this.normalMatrix),this.beforeRenderCallbacks.forEach(o=>o&&o({mesh:this,camera:e}));let r=this.program.cullFace&&this.worldMatrix.determinant()<0;this.program.use({flipFaces:r}),this.geometry.draw({mode:this.mode,program:this.program}),this.afterRenderCallbacks.forEach(o=>o&&o({mesh:this,camera:e}))}}const Cf=new Uint8Array(4);function If(i){return(i&i-1)===0}let K2=1;class ma{constructor(e,{image:r,target:o=e.TEXTURE_2D,type:l=e.UNSIGNED_BYTE,format:c=e.RGBA,internalFormat:h=c,wrapS:m=e.CLAMP_TO_EDGE,wrapT:f=e.CLAMP_TO_EDGE,wrapR:v=e.CLAMP_TO_EDGE,generateMipmaps:x=o===(e.TEXTURE_2D||e.TEXTURE_CUBE_MAP),minFilter:S=x?e.NEAREST_MIPMAP_LINEAR:e.LINEAR,magFilter:T=e.LINEAR,premultiplyAlpha:R=!1,unpackAlignment:P=4,flipY:b=o==(e.TEXTURE_2D||e.TEXTURE_3D),anisotropy:A=0,level:F=0,width:se,height:q=se,length:B=1}={}){this.gl=e,this.id=K2++,this.image=r,this.target=o,this.type=l,this.format=c,this.internalFormat=h,this.minFilter=S,this.magFilter=T,this.wrapS=m,this.wrapT=f,this.wrapR=v,this.generateMipmaps=x,this.premultiplyAlpha=R,this.unpackAlignment=P,this.flipY=b,this.anisotropy=Math.min(A,this.gl.renderer.parameters.maxAnisotropy),this.level=F,this.width=se,this.height=q,this.length=B,this.texture=this.gl.createTexture(),this.store={image:null},this.glState=this.gl.renderer.state,this.state={},this.state.minFilter=this.gl.NEAREST_MIPMAP_LINEAR,this.state.magFilter=this.gl.LINEAR,this.state.wrapS=this.gl.REPEAT,this.state.wrapT=this.gl.REPEAT,this.state.anisotropy=0}bind(){this.glState.textureUnits[this.glState.activeTextureUnit]!==this.id&&(this.gl.bindTexture(this.target,this.texture),this.glState.textureUnits[this.glState.activeTextureUnit]=this.id)}update(e=0){const r=!(this.image===this.store.image&&!this.needsUpdate);if((r||this.glState.textureUnits[e]!==this.id)&&(this.gl.renderer.activeTexture(e),this.bind()),!!r){if(this.needsUpdate=!1,this.flipY!==this.glState.flipY&&(this.gl.pixelStorei(this.gl.UNPACK_FLIP_Y_WEBGL,this.flipY),this.glState.flipY=this.flipY),this.premultiplyAlpha!==this.glState.premultiplyAlpha&&(this.gl.pixelStorei(this.gl.UNPACK_PREMULTIPLY_ALPHA_WEBGL,this.premultiplyAlpha),this.glState.premultiplyAlpha=this.premultiplyAlpha),this.unpackAlignment!==this.glState.unpackAlignment&&(this.gl.pixelStorei(this.gl.UNPACK_ALIGNMENT,this.unpackAlignment),this.glState.unpackAlignment=this.unpackAlignment),this.minFilter!==this.state.minFilter&&(this.gl.texParameteri(this.target,this.gl.TEXTURE_MIN_FILTER,this.minFilter),this.state.minFilter=this.minFilter),this.magFilter!==this.state.magFilter&&(this.gl.texParameteri(this.target,this.gl.TEXTURE_MAG_FILTER,this.magFilter),this.state.magFilter=this.magFilter),this.wrapS!==this.state.wrapS&&(this.gl.texParameteri(this.target,this.gl.TEXTURE_WRAP_S,this.wrapS),this.state.wrapS=this.wrapS),this.wrapT!==this.state.wrapT&&(this.gl.texParameteri(this.target,this.gl.TEXTURE_WRAP_T,this.wrapT),this.state.wrapT=this.wrapT),this.wrapR!==this.state.wrapR&&(this.gl.texParameteri(this.target,this.gl.TEXTURE_WRAP_R,this.wrapR),this.state.wrapR=this.wrapR),this.anisotropy&&this.anisotropy!==this.state.anisotropy&&(this.gl.texParameterf(this.target,this.gl.renderer.getExtension("EXT_texture_filter_anisotropic").TEXTURE_MAX_ANISOTROPY_EXT,this.anisotropy),this.state.anisotropy=this.anisotropy),this.image){if(this.image.width&&(this.width=this.image.width,this.height=this.image.height),this.target===this.gl.TEXTURE_CUBE_MAP)for(let o=0;o<6;o++)this.gl.texImage2D(this.gl.TEXTURE_CUBE_MAP_POSITIVE_X+o,this.level,this.internalFormat,this.format,this.type,this.image[o]);else if(ArrayBuffer.isView(this.image))this.target===this.gl.TEXTURE_2D?this.gl.texImage2D(this.target,this.level,this.internalFormat,this.width,this.height,0,this.format,this.type,this.image):(this.target===this.gl.TEXTURE_2D_ARRAY||this.target===this.gl.TEXTURE_3D)&&this.gl.texImage3D(this.target,this.level,this.internalFormat,this.width,this.height,this.length,0,this.format,this.type,this.image);else if(this.image.isCompressedTexture)for(let o=0;o<this.image.length;o++)this.gl.compressedTexImage2D(this.target,o,this.internalFormat,this.image[o].width,this.image[o].height,0,this.image[o].data);else this.target===this.gl.TEXTURE_2D?this.gl.texImage2D(this.target,this.level,this.internalFormat,this.format,this.type,this.image):this.gl.texImage3D(this.target,this.level,this.internalFormat,this.width,this.height,this.length,0,this.format,this.type,this.image);this.generateMipmaps&&(!this.gl.renderer.isWebgl2&&(!If(this.image.width)||!If(this.image.height))?(this.generateMipmaps=!1,this.wrapS=this.wrapT=this.gl.CLAMP_TO_EDGE,this.minFilter=this.gl.LINEAR):this.gl.generateMipmap(this.target)),this.onUpdate&&this.onUpdate()}else if(this.target===this.gl.TEXTURE_CUBE_MAP)for(let o=0;o<6;o++)this.gl.texImage2D(this.gl.TEXTURE_CUBE_MAP_POSITIVE_X+o,0,this.gl.RGBA,1,1,0,this.gl.RGBA,this.gl.UNSIGNED_BYTE,Cf);else this.width?this.target===this.gl.TEXTURE_2D?this.gl.texImage2D(this.target,this.level,this.internalFormat,this.width,this.height,0,this.format,this.type,null):this.gl.texImage3D(this.target,this.level,this.internalFormat,this.width,this.height,this.length,0,this.format,this.type,null):this.gl.texImage2D(this.target,0,this.gl.RGBA,1,1,0,this.gl.RGBA,this.gl.UNSIGNED_BYTE,Cf);this.store.image=this.image}}}class Rf{constructor(e,{width:r=e.canvas.width,height:o=e.canvas.height,target:l=e.FRAMEBUFFER,color:c=1,depth:h=!0,stencil:m=!1,depthTexture:f=!1,wrapS:v=e.CLAMP_TO_EDGE,wrapT:x=e.CLAMP_TO_EDGE,wrapR:S=e.CLAMP_TO_EDGE,minFilter:T=e.LINEAR,magFilter:R=T,type:P=e.UNSIGNED_BYTE,format:b=e.RGBA,internalFormat:A=b,unpackAlignment:F,premultiplyAlpha:se}={}){this.gl=e,this.width=r,this.height=o,this.depth=h,this.stencil=m,this.buffer=this.gl.createFramebuffer(),this.target=l,this.gl.renderer.bindFramebuffer(this),this.textures=[];const q=[];for(let B=0;B<c;B++)this.textures.push(new ma(e,{width:r,height:o,wrapS:v,wrapT:x,wrapR:S,minFilter:T,magFilter:R,type:P,format:b,internalFormat:A,unpackAlignment:F,premultiplyAlpha:se,flipY:!1,generateMipmaps:!1})),this.textures[B].update(),this.gl.framebufferTexture2D(this.target,this.gl.COLOR_ATTACHMENT0+B,this.gl.TEXTURE_2D,this.textures[B].texture,0),q.push(this.gl.COLOR_ATTACHMENT0+B);q.length>1&&this.gl.renderer.drawBuffers(q),this.texture=this.textures[0],f&&(this.gl.renderer.isWebgl2||this.gl.renderer.getExtension("WEBGL_depth_texture"))?(this.depthTexture=new ma(e,{width:r,height:o,minFilter:this.gl.NEAREST,magFilter:this.gl.NEAREST,format:this.stencil?this.gl.DEPTH_STENCIL:this.gl.DEPTH_COMPONENT,internalFormat:e.renderer.isWebgl2?this.stencil?this.gl.DEPTH24_STENCIL8:this.gl.DEPTH_COMPONENT16:this.gl.DEPTH_COMPONENT,type:this.stencil?this.gl.UNSIGNED_INT_24_8:this.gl.UNSIGNED_INT}),this.depthTexture.update(),this.gl.framebufferTexture2D(this.target,this.stencil?this.gl.DEPTH_STENCIL_ATTACHMENT:this.gl.DEPTH_ATTACHMENT,this.gl.TEXTURE_2D,this.depthTexture.texture,0)):(h&&!m&&(this.depthBuffer=this.gl.createRenderbuffer(),this.gl.bindRenderbuffer(this.gl.RENDERBUFFER,this.depthBuffer),this.gl.renderbufferStorage(this.gl.RENDERBUFFER,this.gl.DEPTH_COMPONENT16,r,o),this.gl.framebufferRenderbuffer(this.target,this.gl.DEPTH_ATTACHMENT,this.gl.RENDERBUFFER,this.depthBuffer)),m&&!h&&(this.stencilBuffer=this.gl.createRenderbuffer(),this.gl.bindRenderbuffer(this.gl.RENDERBUFFER,this.stencilBuffer),this.gl.renderbufferStorage(this.gl.RENDERBUFFER,this.gl.STENCIL_INDEX8,r,o),this.gl.framebufferRenderbuffer(this.target,this.gl.STENCIL_ATTACHMENT,this.gl.RENDERBUFFER,this.stencilBuffer)),h&&m&&(this.depthStencilBuffer=this.gl.createRenderbuffer(),this.gl.bindRenderbuffer(this.gl.RENDERBUFFER,this.depthStencilBuffer),this.gl.renderbufferStorage(this.gl.RENDERBUFFER,this.gl.DEPTH_STENCIL,r,o),this.gl.framebufferRenderbuffer(this.target,this.gl.DEPTH_STENCIL_ATTACHMENT,this.gl.RENDERBUFFER,this.depthStencilBuffer))),this.gl.renderer.bindFramebuffer({target:this.target})}setSize(e,r){if(!(this.width===e&&this.height===r)){this.width=e,this.height=r,this.gl.renderer.bindFramebuffer(this);for(let o=0;o<this.textures.length;o++)this.textures[o].width=e,this.textures[o].height=r,this.textures[o].needsUpdate=!0,this.textures[o].update(),this.gl.framebufferTexture2D(this.target,this.gl.COLOR_ATTACHMENT0+o,this.gl.TEXTURE_2D,this.textures[o].texture,0);this.depthTexture?(this.depthTexture.width=e,this.depthTexture.height=r,this.depthTexture.needsUpdate=!0,this.depthTexture.update(),this.gl.framebufferTexture2D(this.target,this.gl.DEPTH_ATTACHMENT,this.gl.TEXTURE_2D,this.depthTexture.texture,0)):(this.depthBuffer&&(this.gl.bindRenderbuffer(this.gl.RENDERBUFFER,this.depthBuffer),this.gl.renderbufferStorage(this.gl.RENDERBUFFER,this.gl.DEPTH_COMPONENT16,e,r)),this.stencilBuffer&&(this.gl.bindRenderbuffer(this.gl.RENDERBUFFER,this.stencilBuffer),this.gl.renderbufferStorage(this.gl.RENDERBUFFER,this.gl.STENCIL_INDEX8,e,r)),this.depthStencilBuffer&&(this.gl.bindRenderbuffer(this.gl.RENDERBUFFER,this.depthStencilBuffer),this.gl.renderbufferStorage(this.gl.RENDERBUFFER,this.gl.DEPTH_STENCIL,e,r))),this.gl.renderer.bindFramebuffer({target:this.target})}}}class X2 extends um{constructor(e,{attributes:r={}}={}){Object.assign(r,{position:{size:2,data:new Float32Array([-1,-1,3,-1,-1,3])},uv:{size:2,data:new Float32Array([0,0,2,0,0,2])}}),super(e,r)}}const Nf={plasma:{color:"#F25BD0",strands:6,crackle:.85,flares:.65,glow:.9,sparks:.6,particleCount:15e3,fill:.5,motion:"rise",particleShape:"square",depth:.6,sway:.5,twinkle:.5,haze:.7,dustSpeed:1},aurora:{color:"#5CFFC8",strands:5,crackle:.6,flares:.5,glow:.8,sparks:.45,particleCount:15e3,fill:.5,motion:"rise",particleShape:"square",depth:.6,sway:.5,twinkle:.5,haze:.7,dustSpeed:1},nebula:{color:"#9478FF",strands:6,crackle:1,flares:.5,glow:.9,sparks:.6,particleCount:18e3,fill:.45,motion:"rise",particleShape:"square",depth:.5,sway:.4,twinkle:.6,haze:.8,dustSpeed:1.2},ember:{color:"#FF8A2A",strands:5,crackle:.9,flares:.8,glow:1,sparks:.8,particleCount:12e3,fill:.35,motion:"rise",particleShape:"round",depth:.7,sway:.3,twinkle:.7,haze:.9,dustSpeed:1.6},frost:{color:"#BFE6FF",strands:3,crackle:.3,flares:.3,glow:.6,sparks:.2,particleCount:16e3,fill:.6,motion:"fall",particleShape:"round",depth:.8,sway:.4,twinkle:.4,haze:.5,dustSpeed:.7},solar:{color:"#FFD36E",strands:6,crackle:.7,flares:1,glow:1.1,sparks:.5,particleCount:15e3,fill:.55,motion:"orbit",particleShape:"square",depth:.6,sway:.7,twinkle:.5,haze:.8,dustSpeed:1},eclipse:{color:"#FFFFFF",strands:4,crackle:.5,flares:.4,glow:.7,sparks:.35,particleCount:14e3,fill:.5,motion:"drift",particleShape:"square",depth:.7,sway:.5,twinkle:.5,haze:.5,dustSpeed:.8},abyss:{color:"#3F7BFF",strands:5,crackle:.55,flares:.6,glow:.9,sparks:.4,particleCount:2e4,fill:.8,motion:"orbit",particleShape:"round",depth:.8,sway:.8,twinkle:.5,haze:.6,dustSpeed:.9}},Y2={rise:0,fall:1,drift:2,orbit:3},Q2={square:0,round:1},fm=8,yu=4,J2=4e4,Ur=256,Z2=45e5,ex=2.2,tx=7,ea=[1,1,1],wu=[0,0,0],tt=(i,e,r)=>Math.min(Math.max(i,e),r),ir=(i,e,r)=>{const o=tt((r-i)/(e-i),0,1);return o*o*(3-2*o)},Pf=i=>1-Math.pow(1-i,3),zi=(i,e,r)=>i.map((o,l)=>o+(e[l]-o)*r),Af=i=>i-Math.PI*2*Math.floor((i+Math.PI)/(Math.PI*2)),nx=(i,e)=>{try{const r=document.createElement("canvas").getContext("2d");if(!r)return e;r.fillStyle="#000000",r.fillStyle=i;const o=r.fillStyle;if(o.startsWith("#")){const c=parseInt(o.slice(1),16);return[(c>>16&255)/255,(c>>8&255)/255,(c&255)/255]}const l=o.match(/[\d.]+/g);return!l||l.length<3?e:[Number(l[0])/255,Number(l[1])/255,Number(l[2])/255]}catch{return e}},rx=i=>i<=.04045?i/12.92:Math.pow((i+.055)/1.055,2.4),ix=i=>i<=.0031308?i*12.92:1.055*Math.pow(i,1/2.4)-.055,Os=i=>{const[e,r,o]=i.map(rx),l=Math.cbrt(.4122214708*e+.5363325363*r+.0514459929*o),c=Math.cbrt(.2119034982*e+.6806995451*r+.1073969566*o),h=Math.cbrt(.0883024619*e+.2817188376*r+.6299787005*o);return[.2104542553*l+.793617785*c-.0040720468*h,1.9779984951*l-2.428592205*c+.4505937099*h,.0259040371*l+.7827717662*c-.808675766*h]},Gu=([i,e,r])=>{const o=Math.pow(i+.3963377774*e+.2158037573*r,3),l=Math.pow(i-.1055613458*e-.0638541728*r,3),c=Math.pow(i-.0894841775*e-1.291485548*r,3);return[4.0767416621*o-3.3077115913*l+.2309699292*c,-1.2684380046*o+2.6097574011*l-.3413193965*c,-.0041960863*o-.7034186147*l+1.707614701*c].map(h=>tt(ix(tt(h,0,1)),0,1))},Mf=(i,e,r)=>Gu(zi(Os(i),Os(e),r)),Fi=(i,e,r,o)=>{const[l,c,h]=Os(i),m=Math.hypot(c,h)*o,f=Math.atan2(h,c)+e*Math.PI/180;return Gu([tt(l+r,0,1),m*Math.cos(f),m*Math.sin(f)])},In=(i,e,r,o)=>{const[,l,c]=Os(i),h=Math.max(Math.hypot(l,c)*o,.02),m=Math.atan2(c,l)+e*Math.PI/180;return Gu([tt(r,0,1),h*Math.cos(m),h*Math.sin(m)])},sx=(i,e)=>{if(e){const r=In(i,0,Math.min(Os(i)[0],.62),1.15);return{rim:r,rimHot:r,rimMid:r,rimDeep:In(i,0,.72,.8),spark:In(i,0,.6,1.2),sparkGlow:In(i,0,.78,.8),haze:In(i,0,.8,.6),edge:In(i,0,.72,.8),tones:[In(i,0,.56,1.1),In(i,16,.6,1.05),In(i,-16,.5,1.1),In(i,0,.66,.9),In(i,0,.74,.7)]}}return{rim:i,rimHot:zi(i,ea,.72),rimMid:zi(i,wu,.15),rimDeep:zi(i,wu,.45),spark:zi(i,ea,.45),sparkGlow:Fi(i,0,-.15,1),haze:zi(i,wu,.6),edge:Fi(i,0,-.3,.9),tones:[Fi(i,0,-.06,1),Fi(i,16,-.02,1),Fi(i,-16,-.12,1.05),Fi(Mf(i,ea,.25),0,.04,1),Mf(i,ea,.7)]}},qu=i=>{let e=i>>>0;return()=>{e=e+1831565813>>>0;let r=e;return r=Math.imul(r^r>>>15,r|1),r^=r+Math.imul(r^r>>>7,r|61),((r^r>>>14)>>>0)/4294967296}},ox=()=>{const i=qu(99),e=[[6,12,.6,1.6],[18,34,1.5,3.5],[40,70,3,7],[80,130,6,12]],r={harmonics:[],rates:[],phases:[],flareHarmonics:[],flareRates:[],flarePhases:[]};for(let o=0;o<fm;o++){e.forEach(([c,h,m,f])=>{r.harmonics.push(Math.round(c+i()*(h-c))),r.rates.push((m+i()*(f-m))*(i()<.5?-1:1)),r.phases.push(i()*Math.PI*2)});for(let c=0;c<3;c++)r.flareHarmonics.push(4+Math.floor(i()*6)),r.flareRates.push((.4+i()*.8)*(i()<.5?-1:1)),r.flarePhases.push(i()*Math.PI*2);const l=o===0;r.flareHarmonics.push(l?.75:.95+i()*.3),r.flareRates.push(l?1.15:.8+i()*.2),r.flarePhases.push(l?1:.7+i()*.25)}return r},ax=i=>{const e=qu(1337),r=Math.max(1,Math.ceil(i/Ur)),o=new Float32Array(Ur*r*4),l=new Float32Array(Ur*r*4);let c=0,h=0;for(;c<i&&h<i*80;){h++;let m,f,v;if(e()<.28){const S=e()*Math.PI*2,T=.87+Math.sqrt(e())*.105;if(m=Math.cos(S)*T,f=Math.sin(S)*T,e()>ir(-.6,.3,-f))continue;const R=e();v=R<.5?3:R<.8?2:1}else{m=e()*2-1,f=e()*2-1;const S=Math.hypot(m,f);if(S>.975)continue;const T=Math.pow(ir(-.25,.85,-f),1.3),R=ir(.66,.96,S)*ir(-.7,.3,-f),P=Math.max(T,R*.9);if(e()>.012+.988*P)continue;if(P<.12)v=4;else{const b=e();v=b<.32?0:b<.52?1:b<.8?2:3}}const x=Math.sqrt(Math.max(0,.95-m*m-f*f));o[c*4]=m,o[c*4+1]=f,o[c*4+2]=(e()*2-1)*x,o[c*4+3]=v,l[c*4]=v===4?1.8:e()<.22?2.1:1.3,l[c*4+1]=e(),l[c*4+2]=2.5+e()*3.5,l[c*4+3]=.16+e()*.26,c++}return{home:o,seed:l,count:c,rows:r}},xu=`#version 300 es
in vec2 position;
in vec2 uv;
out vec2 vUv;
void main() {
  vUv = uv;
  gl_Position = vec4(position, 0.0, 1.0);
}
`,Ku=`
uint scramble(uint v) {
  v = v * 747796405u + 2891336453u;
  uint w = ((v >> ((v >> 28u) + 4u)) ^ v) * 277803737u;
  return (w >> 22u) ^ w;
}

float random(uint v) {
  return float(scramble(v)) * (1.0 / 4294967295.0);
}
`,pm=`
uniform float uDustTime;
uniform vec2 uTurn;
uniform float uMotion;
uniform float uFill;

vec3 settle(vec3 p, out float spread) {
  float bend = exp2((0.5 - uFill) * 1.8);
  float h = clamp((p.y + 1.0) * 0.5, 0.0, 1.0);
  float y = 2.0 * pow(h, bend) - 1.0;
  float from = sqrt(max(1.0 - p.y * p.y, 1e-4));
  float to = sqrt(max(1.0 - y * y, 0.0));
  spread = clamp(bend * pow(max(h, 1e-3), bend - 1.0) * to / from, 0.25, 1.0);
  return vec3(p.xz * (to / from), y).xzy;
}

vec3 drift(vec4 home, vec4 seed, uint id, out float life, out float spread) {
  vec3 p = settle(home.xyz, spread);
  float t = uDustTime;
  float u = fract(t / seed.z + seed.y);
  life = sin(3.14159265 * u);
  float travel = seed.w;
  if (uMotion < 0.5) {
    p.y += travel * (u - 0.5);
  } else if (uMotion < 1.5) {
    p.y -= travel * (u - 0.5);
  } else if (uMotion < 2.5) {
    p += 0.045 * vec3(
      sin(t * 0.37 + seed.y * 17.0) + 0.5 * sin(t * 0.83 + seed.z * 5.0),
      sin(t * 0.29 + seed.z * 11.0) + 0.5 * sin(t * 0.61 + seed.w * 7.0),
      sin(t * 0.33 + seed.w * 23.0)
    );
  } else {
    float loop = t * (0.6 + 0.9 * random(id * 7u + 3u)) * (random(id * 7u + 10u) < 0.5 ? -1.0 : 1.0) + seed.y * 6.2831853;
    p.xy += (0.025 + 0.05 * random(id * 7u + 16u)) * vec2(cos(loop), sin(loop));
  }
  float wobble = 0.002 + 0.006 * random(id * 7u + 1u);
  float w1 = 0.8 + 2.4 * random(id * 7u + 2u);
  float w2 = 0.8 + 2.4 * random(id * 7u + 4u);
  p += wobble * vec3(sin(t * w1 + seed.y * 40.0), cos(t * w2 + seed.z * 30.0), sin(t * (w1 + w2) * 0.5 + seed.w * 20.0));
  float cy = cos(uTurn.x);
  float sy = sin(uTurn.x);
  p.xz = mat2(cy, -sy, sy, cy) * p.xz;
  float cx = cos(uTurn.y);
  float sx = sin(uTurn.y);
  p.yz = mat2(cx, -sx, sx, cx) * p.yz;
  return p;
}
`,lx=`#version 300 es
precision highp float;

uniform vec2 uCenter;
uniform float uRadius;
uniform float uDpr;
uniform float uLine;
uniform float uTime;
uniform float uFrame;
uniform float uBins;
uniform float uStrands;
uniform float uCrackle;
uniform float uFlares;
uniform float uGlow;
uniform float uHaze;
uniform float uFill;
uniform float uPresence;
uniform float uUnfold;
uniform float uBloom;
uniform float uInside;
uniform float uEncode;
uniform vec3 uRim;
uniform vec3 uRimHot;
uniform vec3 uRimMid;
uniform vec3 uRimDeep;
uniform vec3 uSpark;
uniform vec3 uSparkGlow;
uniform vec3 uHazeColor;
uniform vec3 uEdgeColor;
uniform vec4 uHeat;
uniform vec4 uHarmonics[8];
uniform vec4 uRates[8];
uniform vec4 uPhases[8];
uniform vec4 uFlareHarmonics[8];
uniform vec4 uFlareRates[8];
uniform vec4 uFlarePhases[8];
uniform vec4 uArcs[4];

out vec4 fragColor;
${Ku}
const float PI = 3.14159265;
const float TAU = 6.28318531;
const vec4 AMPS = vec4(0.35, 0.3, 0.22, 0.13);

float bell(float d, float w) {
  float x = d / w;
  return exp(-x * x);
}

float segment(vec2 p, vec2 a, vec2 b) {
  vec2 pa = p - a;
  vec2 ba = b - a;
  float h = clamp(dot(pa, ba) / max(dot(ba, ba), 1e-5), 0.0, 1.0);
  return length(pa - ba * h);
}

float pool(vec2 q) {
  float t = length(q - vec2(0.0, mix(-1.0, -0.66, uFill))) / mix(0.8, 1.35, uFill);
  return t < 0.6 ? mix(0.5, 0.22, t / 0.6) : mix(0.22, 0.0, clamp((t - 0.6) / 0.4, 0.0, 1.0));
}

void main() {
  vec2 p = gl_FragCoord.xy / uDpr - uCenter;
  float r = length(p);
  float R = uRadius;
  float theta = atan(p.y, p.x);
  float lift = p.y / max(r, 1e-3);
  float topDim = 1.0 - 0.35 * pow(max(lift, 0.0), 1.5);
  vec3 col = vec3(0.0);
  float hot = 0.0;
  uint frame = uint(uFrame);

  if (r < R) {
    vec2 q = p / R;
    float chord = sqrt(max(1.0 - dot(q, q), 0.0));
    float haze = pool(q) * (0.55 + 0.45 * chord);
    col += uHazeColor * haze * uHaze * uInside;
    float e = length(q - vec2(0.0, 0.2)) / 1.2;
    float edge = 0.5 * pow(smoothstep(0.62, 1.0, e), 1.4);
    col += uEdgeColor * edge * uInside * (0.5 + 0.5 * uHaze);
  }

  float dr = r - R;
  float halo = 1.0 - smoothstep(R * 0.05, R * 0.105, abs(dr - R * 0.0213));
  col += uRimDeep * 0.18 * halo * topDim * uGlow * uBloom;
  col += uRim * 0.12 * bell(dr + R * 0.0383, R * 0.032) * uGlow * uBloom;
  col += uRim * 0.32 * bell(dr, max(R * 0.0117, uLine)) * uPresence * uUnfold;

  float delta = mod(theta - uHeat.x + PI, TAU) - PI;
  float heat = uHeat.z * uHeat.y * exp(-delta * delta / 0.3);
  float crackle = uCrackle + heat * 0.9;
  float amp = R * 0.016 * (0.3 + 1.4 * crackle) * uUnfold;
  float jitterAmp = R * 0.0048 * (0.3 + 1.4 * uCrackle) * uUnfold * (1.0 + heat * 0.3);
  float flareAmp = R * 0.064 * (0.4 + 1.2 * crackle) * uFlares * 1.6 * uUnfold;

  if (abs(dr) < amp * 2.0 + flareAmp + R * 0.3) {
    float step = TAU / uBins;
    float binPos = (theta + PI) / step;
    float bin0 = floor(binPos);
    float binF = binPos - bin0;
    float th0 = bin0 * step - PI;
    float th1 = th0 + step;
    uint b0 = uint(mod(bin0, uBins));
    uint b1 = uint(mod(bin0 + 1.0, uBins));
    float gain = min(1.0, 2.4 / max(uStrands, 1.0));
    for (int k = 0; k < 8; k++) {
      if (float(k) >= uStrands) break;
      vec4 m = uHarmonics[k];
      vec4 lead = uRates[k] * uTime + uPhases[k];
      float wave0 = dot(AMPS, sin(m * th0 + lead));
      float wave1 = dot(AMPS, sin(m * th1 + lead));
      uint salt = uint(k) * 1013u + frame * 7919u;
      vec4 shape = uFlareHarmonics[k];
      vec4 look = uFlareRates[k];
      vec4 tone = uFlarePhases[k];
      float a = amp * shape.w;
      float off0 = a * wave0 + jitterAmp * (random(b0 + salt) - 0.5);
      float off1 = a * wave1 + jitterAmp * (random(b1 + salt) - 0.5);
      float rc = R + mix(off0, off1, binF);
      float grade = (off1 - off0) / (step * max(r, 1.0));
      float d = abs(r - rc) * inversesqrt(1.0 + grade * grade);
      float swell = 0.8 + 0.4 * (0.5 + 0.5 * sin(3.0 * theta + uTime * 0.7 + tone.x * 1.7));
      float width = uLine * look.w * swell * (1.0 + heat * 0.25);
      float core = exp(-d * d / (width * width));
      float sheath = exp(-d * d / (width * width * 3.0));
      float bright = tone.w * (1.0 + heat * 0.45) * uPresence;
      col += (uRimHot * core * 0.8 + uRim * sheath * 0.32) * bright;
      hot += core * bright;
      vec3 fargs = shape.xyz * theta + look.xyz * uTime + tone.xyz;
      float flare = max(0.0, (sin(fargs.x) + sin(fargs.y) + sin(fargs.z)) / 3.0);
      flare = (flare * flare + heat * 0.35) * flareAmp;
      float dw = abs(r - rc - flare);
      float dm = abs(r - rc - flare * 0.6);
      float dn = abs(r - rc - flare * 0.25);
      vec3 glow = uRimDeep * (0.07 * bell(dw, R * 0.09) + 0.16 * bell(dw, R * 0.05));
      glow += uRimMid * 0.28 * bell(dm, R * 0.027) + uRim * 0.38 * bell(dn, R * 0.013);
      col += glow * gain * topDim * uGlow * uBloom * (1.0 + heat * 1.4);
    }
  }

  for (int i = 0; i < 4; i++) {
    vec4 arc = uArcs[i];
    if (arc.w <= 0.002) continue;
    float mid = arc.x + arc.y * 0.5;
    vec2 center = R * 0.93 * vec2(cos(mid), sin(mid));
    if (distance(p, center) > R * (abs(arc.y) * 0.6 + 0.1) + 12.0) continue;
    float ar = R * 0.955;
    vec2 a0 = ar * vec2(cos(arc.x), sin(arc.x));
    vec2 a2 = ar * vec2(cos(arc.x + arc.y), sin(arc.x + arc.y));
    vec2 a1 = R * (0.955 - arc.z) * vec2(cos(mid), sin(mid));
    float dmin = 1e5;
    float along = 0.0;
    vec2 prev = a0;
    for (int s = 1; s <= 10; s++) {
      float u = float(s) / 10.0;
      vec2 b = mix(mix(a0, a1, u), mix(a1, a2, u), u);
      vec2 pa = p - prev;
      vec2 ba = b - prev;
      float h = clamp(dot(pa, ba) / max(dot(ba, ba), 1e-5), 0.0, 1.0);
      float dist = length(pa - ba * h);
      if (dist < dmin) {
        dmin = dist;
        along = (float(s) - 1.0 + h) / 10.0;
      }
      prev = b;
    }
    float taper = sqrt(max(sin(PI * along), 0.0));
    float arcWidth = uLine * (0.55 + 0.6 * taper);
    float arcCore = exp(-dmin * dmin / (arcWidth * arcWidth));
    float arcGlow = exp(-dmin * dmin / (arcWidth * arcWidth * 12.0));
    col += (uSpark * 0.95 * arcCore + uSparkGlow * 0.4 * arcGlow) * arc.w * taper;
    hot += arcCore * arc.w * taper * 0.6;
  }

  fragColor = vec4(col, hot) * uEncode;
}
`,ux=`#version 300 es
precision highp float;

in float aIndex;

uniform sampler2D tHome;
uniform sampler2D tSeed;
uniform sampler2D tOffset;
uniform float uStirred;
uniform vec2 uCenter;
uniform vec2 uViewport;
uniform float uRadius;
uniform float uDpr;
uniform float uDepth;
uniform float uTwinkle;
uniform float uPointScale;
uniform float uReveal;
uniform float uEncode;
uniform vec3 uTones[5];
uniform vec3 uRimTone;

out vec3 vColor;
out float vSize;
${Ku}
${pm}
void main() {
  ivec2 cell = ivec2(int(mod(aIndex, ${Ur}.0)), int(floor(aIndex / ${Ur}.0)));
  uint id = uint(aIndex);
  vec4 home = texelFetch(tHome, cell, 0);
  vec4 seed = texelFetch(tSeed, cell, 0);
  float life;
  float spread;
  vec3 p = drift(home, seed, id, life, spread);
  if (uStirred > 0.5) p += texelFetch(tOffset, cell, 0).xyz;
  float len = length(p);
  float inside = 1.0 - smoothstep(0.955, 0.985, length(p.xy));
  if (len > 0.975) p *= 0.975 / len;

  float front = p.z * 0.5 + 0.5;
  float depthSize = mix(1.0, 0.7 + 0.6 * front, uDepth);
  float depthLight = mix(1.0, 0.35 + 0.8 * front, uDepth);
  float blink = sin(uDustTime * (2.0 + 6.0 * random(id * 7u + 5u)) + random(id * 7u + 6u) * 6.2831853);
  float twinkle = mix(1.0, smoothstep(-0.9, -0.6, blink), uTwinkle);
  float fade = smoothstep(0.04, 0.12, life);
  float order = (home.y + 1.0) * 0.5 * 0.55 + random(id * 7u + 8u) * 0.25;
  float reveal = smoothstep(order, order + 0.2, uReveal * 1.0);
  float alpha = random(id * 7u + 9u) < 0.5 || home.w > 3.5 ? 1.0 : 0.6;

  float size = seed.x * uPointScale * (0.35 + 0.95 * life) * depthSize * mix(0.5, 1.0, reveal);
  vec2 screen = uCenter + p.xy * uRadius;
  gl_Position = vec4(screen / uViewport * 2.0 - 1.0, 0.0, 1.0);
  float px = size * uDpr;
  gl_PointSize = px + 2.0;
  vSize = px;

  int tone = int(home.w + 0.5);
  float rimLit = smoothstep(0.8, 0.97, length(p.xy));
  vec3 color = uTones[tone] + uRimTone * rimLit * rimLit * 0.12;
  vColor = color * alpha * fade * twinkle * depthLight * reveal * inside * sqrt(spread) * uEncode;
}
`,cx=`#version 300 es
precision highp float;

uniform float uShape;

in vec3 vColor;
in float vSize;

out vec4 fragColor;

void main() {
  vec2 q = (gl_PointCoord - 0.5) * (vSize + 2.0);
  float half_ = max(vSize * 0.5, 0.5);
  float cover;
  if (uShape < 0.5) {
    vec2 c = clamp(half_ - abs(q) + 0.5, 0.0, 1.0);
    cover = c.x * c.y;
  } else {
    cover = clamp(half_ - length(q) + 0.5, 0.0, 1.0);
  }
  if (cover <= 0.0) discard;
  fragColor = vec4(vColor * cover, 0.0);
}
`,dx=`#version 300 es
precision highp float;

uniform sampler2D tHome;
uniform sampler2D tSeed;
uniform sampler2D tOffset;
uniform sampler2D tVelocity;
uniform float uDt;
uniform float uReset;
uniform vec4 uBrush;
uniform float uBrushPower;
uniform vec4 uKick;

layout(location = 0) out vec4 outOffset;
layout(location = 1) out vec4 outVelocity;
${Ku}
${pm}
vec3 swirl(vec3 p) {
  float t = uDustTime * 0.15;
  vec3 a = vec3(1.7, 1.9, 1.5) * p.yzx + vec3(t, 1.2, 2.1);
  vec3 b = vec3(2.3, 2.1, 2.7) * p.zxy + vec3(0.4, t * 1.3, 0.9);
  vec3 ca = cos(a) * vec3(1.7, 1.9, 1.5);
  vec3 cb = cos(b) * vec3(2.3, 2.1, 2.7);
  return vec3(ca.z - cb.x, cb.y - ca.x, ca.y - cb.z);
}

void main() {
  ivec2 cell = ivec2(gl_FragCoord.xy);
  if (uReset > 0.5) {
    outOffset = vec4(0.0);
    outVelocity = vec4(0.0);
    return;
  }
  uint id = uint(cell.y * ${Ur} + cell.x);
  vec4 home = texelFetch(tHome, cell, 0);
  vec4 seed = texelFetch(tSeed, cell, 0);
  vec3 o = texelFetch(tOffset, cell, 0).xyz;
  vec3 v = texelFetch(tVelocity, cell, 0).xyz;
  float life;
  float spread;
  vec3 base = drift(home, seed, id, life, spread);
  vec3 p = base + o;

  float k = mix(0.8, 2.2, random(id * 7u + 11u));
  vec3 acc = -k * o - 1.5 * sqrt(k) * v;

  vec2 gap = p.xy - uBrush.xy;
  float touch = exp(-dot(gap, gap) / 0.07) * uBrushPower;
  acc += (vec3(uBrush.zw, 0.0) - v) * touch * 14.0;
  float pace = length(v);
  if (pace > 1e-4) {
    vec3 heading = v / pace;
    vec3 curl = swirl(p * 1.6);
    acc += (curl - heading * dot(curl, heading)) * min(pace, 2.0) * 1.8;
  }

  if (uKick.z > 0.0) {
    vec3 jolt = vec3(random(id * 7u + 12u), random(id * 7u + 13u), random(id * 7u + 14u)) - 0.5;
    float near = exp(-dot(p.xy - uKick.xy, p.xy - uKick.xy) / 0.4);
    vec3 spinKick = vec3(-p.z, 0.0, p.x) * 0.9;
    vec3 lift = vec3(0.0, 0.5 + 0.8 * random(id * 7u + 15u), 0.0) * (0.3 + 0.7 * smoothstep(0.2, -0.8, p.y));
    v += (jolt * 0.8 + spinKick + lift) * uKick.z * (0.4 + 0.45 * near);
  }

  v += acc * uDt;
  o += v * uDt;
  vec3 q = base + o;
  float len = length(q);
  if (len > 0.97) {
    vec3 n = q / len;
    o -= n * (len - 0.97);
    v -= n * max(dot(v, n), 0.0) * 1.5;
  }
  outOffset = vec4(o, 1.0);
  outVelocity = vec4(v, 1.0);
}
`,hx=`#version 300 es
precision highp float;

uniform sampler2D tScene;
uniform float uLight;
uniform float uDecode;

in vec2 vUv;
out vec4 fragColor;

vec3 soften(vec3 x) {
  vec3 over = max(x - 0.6, 0.0);
  return min(x, 0.6) + 0.4 * (1.0 - exp(-over / 0.4));
}

void main() {
  vec4 scene = texture(tScene, vUv) * uDecode;
  vec3 light = max(scene.rgb, 0.0);
  float peak = max(light.r, max(light.g, light.b));
  if (uLight > 0.5) {
    vec3 hue = light / max(peak, 1e-4);
    float cover = 1.0 - exp(-peak * 2.4);
    vec3 ink = hue * mix(0.92, 0.72, cover);
    float core = clamp(scene.a * 0.7, 0.0, 1.0) * cover;
    vec3 tint = mix(vec3(1.0), hue, 0.22);
    fragColor = vec4(tint * core + ink * cover * (1.0 - core), core + cover * (1.0 - core));
    return;
  }
  light += vec3(max(peak - 1.8, 0.0) * 0.25);
  vec3 shown = soften(light);
  fragColor = vec4(shown, max(shown.r, max(shown.g, shown.b)));
}
`,fx=({preset:i="plasma",color:e,theme:r="dark",size:o=.7,strands:l,crackle:c,flares:h,glow:m,sparks:f,particleCount:v,fill:x,motion:S,particleShape:T,depth:R,sway:P,twinkle:b,haze:A,speed:F=1,dustSpeed:se,interactive:q=!0,hoverStrength:B=.7,intro:W=!0,paused:Q=!1,className:pe="",style:de})=>{const w=ne.useRef(null),Ne=ne.useRef(null),we=ne.useRef(null),ye=Nf[i]||Nf.plasma,me=(Pe,Ce)=>Pe??ye[Ce],ue=me(e,"color"),Ve=ne.useMemo(()=>{const Pe=r==="light";return{light:Pe,palette:sx(nx(ue,[.95,.36,.82]),Pe)}},[ue,r]);return ne.useEffect(()=>{var Pe;Ne.current={...Ve,size:o,strands:me(l,"strands"),crackle:me(c,"crackle"),flares:me(h,"flares"),glow:me(m,"glow"),sparks:me(f,"sparks"),particleCount:me(v,"particleCount"),fill:me(x,"fill"),motion:me(S,"motion"),particleShape:me(T,"particleShape"),depth:me(R,"depth"),sway:me(P,"sway"),twinkle:me(b,"twinkle"),haze:me(A,"haze"),dustSpeed:me(se,"dustSpeed"),speed:F,interactive:q,hoverStrength:B,intro:W,paused:Q},(Pe=we.current)==null||Pe.call(we)}),ne.useEffect(()=>{var Hs,bn;const Pe=w.current;if(!Pe)return;let Ce;try{Ce=new Yw({alpha:!0,premultipliedAlpha:!0,antialias:!1,depth:!1})}catch{return}const E=Ce.gl;if(!Ce.isWebgl2){(Hs=E.getExtension("WEBGL_lose_context"))==null||Hs.loseContext();return}const ee=E.canvas;ee.style.display="block",ee.style.width="100%",ee.style.height="100%",ee.setAttribute("aria-hidden","true"),Pe.appendChild(ee);const Y=!!E.getExtension("EXT_color_buffer_float"),C=Y||!!E.getExtension("EXT_color_buffer_half_float"),O=C?1:.25,Se=new X2(E),fe=new ma(E),ke=ox(),xe=new Rf(E,{width:1,height:1,depth:!1,type:C?E.HALF_FLOAT:E.UNSIGNED_BYTE,format:E.RGBA,internalFormat:C?E.RGBA16F:E.RGBA,minFilter:E.NEAREST,magFilter:E.NEAREST}),Me=new Array(yu*4).fill(0),te={uCenter:{value:[0,0]},uRadius:{value:1},uDpr:{value:1},uLine:{value:.6},uTime:{value:0},uFrame:{value:0},uBins:{value:420},uStrands:{value:5},uCrackle:{value:.6},uFlares:{value:.5},uGlow:{value:.8},uHaze:{value:.7},uFill:{value:.5},uPresence:{value:0},uUnfold:{value:0},uBloom:{value:0},uInside:{value:0},uEncode:{value:O},uRim:{value:[1,1,1]},uRimHot:{value:[1,1,1]},uRimMid:{value:[1,1,1]},uRimDeep:{value:[1,1,1]},uSpark:{value:[1,1,1]},uSparkGlow:{value:[1,1,1]},uHazeColor:{value:[0,0,0]},uEdgeColor:{value:[0,0,0]},uHeat:{value:[0,0,0,0]},uHarmonics:{value:ke.harmonics},uRates:{value:ke.rates},uPhases:{value:ke.phases},uFlareHarmonics:{value:ke.flareHarmonics},uFlareRates:{value:ke.flareRates},uFlarePhases:{value:ke.flarePhases},uArcs:{value:Me}},Le={uDustTime:{value:0},uTurn:{value:[0,0]},uMotion:{value:0},uFill:te.uFill,tHome:{value:fe},tSeed:{value:fe}},Ue={...Le,tOffset:{value:fe},uStirred:{value:0},uCenter:te.uCenter,uViewport:{value:[1,1]},uRadius:te.uRadius,uDpr:te.uDpr,uDepth:{value:.6},uTwinkle:{value:.5},uPointScale:{value:1},uReveal:{value:0},uEncode:{value:O},uTones:{value:new Array(15).fill(1)},uRimTone:{value:[1,1,1]},uShape:{value:0}},He={...Le,tOffset:{value:fe},tVelocity:{value:fe},uDt:{value:.016},uReset:{value:1},uBrush:{value:[0,0,0,0]},uBrushPower:{value:0},uKick:{value:[0,0,0,0]}},nt={tScene:{value:xe.texture},uLight:{value:0},uDecode:{value:1/O}},Qe=Oe=>(Oe.setBlendFunc(E.ONE,E.ONE),Oe),Be=new Zo(E,{geometry:Se,program:Qe(new Jo(E,{vertex:xu,fragment:lx,uniforms:te,transparent:!0,depthTest:!1,depthWrite:!1}))}),sn=Qe(new Jo(E,{vertex:ux,fragment:cx,uniforms:Ue,transparent:!0,depthTest:!1,depthWrite:!1})),vt=C?new Zo(E,{geometry:Se,program:new Jo(E,{vertex:xu,fragment:dx,uniforms:He,depthTest:!1,depthWrite:!1})}):null,qt=new Zo(E,{geometry:Se,program:new Jo(E,{vertex:xu,fragment:hx,uniforms:nt,depthTest:!1,depthWrite:!1})}),Mn=Oe=>{Oe&&(E.deleteFramebuffer(Oe.buffer),Oe.textures.forEach(ce=>E.deleteTexture(ce.texture)))},Hn=Oe=>new Rf(E,{width:Ur,height:Oe,color:2,depth:!1,type:Y?E.FLOAT:E.HALF_FLOAT,format:E.RGBA,internalFormat:Y?E.RGBA32F:E.RGBA16F,minFilter:E.NEAREST,magFilter:E.NEAREST}),on=(Oe,ce)=>new ma(E,{image:Oe,width:Ur,height:ce,type:E.FLOAT,format:E.RGBA,internalFormat:E.RGBA32F,minFilter:E.NEAREST,magFilter:E.NEAREST,generateMipmaps:!1,flipY:!1});let Fe=null;const Ot=()=>{Fe&&(Fe.mesh.geometry.remove(),E.deleteTexture(Fe.home.texture),E.deleteTexture(Fe.seed.texture),Mn(Fe.read),Mn(Fe.write),Fe=null)},an=()=>{!vt||!Fe||!Fe.read||!Fe.write||(He.tOffset.value=fe,He.tVelocity.value=fe,He.uReset.value=1,Ce.render({scene:vt,target:Fe.read,clear:!1}),Ce.render({scene:vt,target:Fe.write,clear:!1}),He.uReset.value=0)},Wn=Oe=>{const ce=tt(Math.round(Oe/100)*100,0,J2);if(Fe&&Fe.requested===ce)return;if(Ot(),!ce){Fe=null;return}const Ae=ax(ce),Pt=new Float32Array(Ae.count);for(let Yt=0;Yt<Ae.count;Yt++)Pt[Yt]=Yt;const At=new um(E,{aIndex:{size:1,data:Pt}});Fe={requested:ce,rows:Ae.rows,home:on(Ae.home,Ae.rows),seed:on(Ae.seed,Ae.rows),mesh:new Zo(E,{mode:E.POINTS,geometry:At,program:sn}),read:vt?Hn(Ae.rows):null,write:vt?Hn(Ae.rows):null},Le.tHome.value=Fe.home,Le.tSeed.value=Fe.seed,an(),oe=0},ot=((bn=window.matchMedia)==null?void 0:bn.call(window,"(prefers-reduced-motion: reduce)").matches)??!1,it=qu(913);let ft=1,at=1,Kt=0,Ft=performance.now(),Nt=0,Et=0,L=0,G=0,j=!0,V=!0,J=0,oe=0,Te=0,De=null,D=.3;const K=[],H={x:0,y:0,inside:!1,fresh:!0},he={angle:0,velocity:0,power:0,near:0},_e={x:0,y:0,vx:0,vy:0},Re={x:0,y:0,vx:0,vy:0},yt=()=>{ft=Math.max(1,Pe.clientWidth),at=Math.max(1,Pe.clientHeight),Ce.dpr=Math.min(window.devicePixelRatio||1,2,Math.sqrt(Z2/(ft*at))),Ce.setSize(ft,at),xe.setSize(E.canvas.width,E.canvas.height),lt()},Xt=(Oe,ce)=>{K.length>=yu||K.push({start:Oe,span:(.05+it()*.07)*(it()<.5?-1:1),curl:.02+it()*.04,life:0,duration:.2+it()*.2,drift:(it()-.5)*.3,strength:ce})},ln=Oe=>{if(Kt=0,!V)return;const ce=Ne.current,Ae=Math.min(.05,Math.max(1/240,(Oe-Ft)/1e3));if(Ft=Oe,!ce)return;const Pt=!ce.paused&&!ot;G=ce.intro&&!ot?Math.min(1,G+Ae/ex):1;const At=Pf(ir(0,.42,G)),Yt=Pf(ir(0,.32,G)),di=Math.sin(Math.PI*ir(.22,.78,G))*.35,Qt=Math.max(8,tt(ce.size,.1,1.5)*Math.min(ft,at)/2),fr=ce.interactive&&!ot?tt(ce.hoverStrength,0,1):0,Ge=H.x-ft/2,hi=at/2-H.y,Gi=Math.hypot(Ge,hi),fi=H.inside?fr:0;he.power<.02&&(he.angle=Math.atan2(hi,Ge),he.velocity=0);const pi=Af(Math.atan2(hi,Ge)-he.angle);he.velocity+=(120*pi-19*he.velocity)*Ae,he.angle=Af(he.angle+he.velocity*Ae),he.power+=(fi-he.power)*(1-Math.exp(-Ae/(fi>he.power?.3:.55)));const _a=Math.exp(-Math.pow((Gi-Qt)/(Qt*.45),2));he.near+=(_a-he.near)*(1-Math.exp(-Ae/.15)),J*=Math.exp(-Ae/.7);const qn=Ge/Qt,wn=hi/Qt;Math.hypot(qn-_e.x,wn-_e.y)>.6&&(H.fresh=!0),H.fresh&&(_e.x=qn,_e.y=wn,_e.vx=0,_e.vy=0,H.fresh=!1);const Jt=1-Math.exp(-Ae/.05);_e.vx+=((qn-_e.x)/Ae-_e.vx)*Jt,_e.vy+=((wn-_e.y)/Ae-_e.vy)*Jt,_e.x=qn,_e.y=wn;const qi=Math.hypot(_e.vx,_e.vy),jt=qi>4?4/qi:1,Ea=Math.exp(-Math.max(0,Math.hypot(qn,wn)-1)*6),Ws=H.inside?fr*Ea*At:0;if(Te=Te*Math.exp(-Ae/1.2)+Ws*Math.min(qi,4)*Ae,Pt){const Ut=1+J*.6+he.power*he.near*.3,ct=Ae*Math.max(0,ce.speed)*2*Ut;Nt+=ct,Et+=Ae*Math.max(0,ce.dustSpeed)*(1+J*.4),L+=Ae*Math.max(0,ce.dustSpeed);const Wr=tt(ce.crackle+J*.5,0,1.5);if(ce.sparks>.01&&G>.55&&(D-=ct*ce.sparks*2*(.6+Wr*.6),D<=0)){const Kn=he.power*he.near,xn=it()<Kn*.7?he.angle+(it()-.5)*.8:it()<.7?Math.PI/2+(it()-.5)*1.5:it()*Math.PI*2;Xt(xn,.8+Kn*.6+J*.4),D=.15+it()*.6}for(let Kn=K.length-1;Kn>=0;Kn--){const xn=K[Kn];xn.life+=ct,xn.start+=xn.drift*ct,xn.life>=xn.duration&&K.splice(Kn,1)}}else K.length=0;for(let Ut=0;Ut<yu;Ut++){const ct=K[Ut];Me[Ut*4]=ct?ct.start:0,Me[Ut*4+1]=ct?ct.span:0,Me[Ut*4+2]=ct?ct.curl:0,Me[Ut*4+3]=ct?Math.sin(Math.PI*ct.life/ct.duration)*ct.strength:0}Wn(ce.particleCount);const cn=ce.palette;te.uCenter.value=[ft/2,at/2],te.uRadius.value=Qt,te.uDpr.value=Ce.dpr,te.uLine.value=Math.max(.6,Qt*.0035),te.uTime.value=Nt,te.uFrame.value=Math.floor(Nt*24)%1e5,te.uBins.value=tt(Math.round(Math.PI*2*Qt/2.6),240,900),te.uStrands.value=Math.round(tt(ce.strands,1,fm)),te.uCrackle.value=tt(ce.crackle,0,1)+J*.5+di,te.uFlares.value=tt(ce.flares,0,1),te.uGlow.value=tt(ce.glow,0,2)*(1+J*.5+di)*(ce.light?.35:1),te.uHaze.value=tt(ce.haze,0,2)*(ce.light?.6:1),te.uFill.value=tt(ce.fill,0,1),te.uPresence.value=At,te.uUnfold.value=Yt,te.uBloom.value=At*At,te.uInside.value=ir(.2,.95,G),te.uRim.value=cn.rim,te.uRimHot.value=cn.rimHot,te.uRimMid.value=cn.rimMid,te.uRimDeep.value=cn.rimDeep,te.uSpark.value=cn.spark,te.uSparkGlow.value=cn.sparkGlow,te.uHazeColor.value=cn.haze,te.uEdgeColor.value=cn.edge,te.uHeat.value=[he.angle,he.near,he.power*At,0],Le.uDustTime.value=Et;const $r=H.inside?fr*At:0,Vr=tt(qn,-1.6,1.6)*$r,pr=tt(wn,-1.6,1.6)*$r;Re.vx+=(40*(Vr-Re.x)-11*Re.vx)*Ae,Re.vy+=(40*(pr-Re.y)-11*Re.vy)*Ae,Re.x+=Re.vx*Ae,Re.y+=Re.vy*Ae;const Hr=tt(ce.sway,0,1);Le.uTurn.value=[Hr*.42*Math.sin(L*.23)+Re.x*.3,Hr*.12*Math.sin(L*.17+1.3)-Re.y*.16],Le.uMotion.value=Y2[ce.motion]??0,Ue.uViewport.value=[ft,at],Ue.uDepth.value=tt(ce.depth,0,1),Ue.uTwinkle.value=tt(ce.twinkle,0,1),Ue.uPointScale.value=Math.max(1,Qt/491),Ue.uReveal.value=ir(.18,1,G),Ue.uTones.value=cn.tones.flat(),Ue.uRimTone.value=cn.rim,Ue.uShape.value=Q2[ce.particleShape]??0;const kt=Fe;kt&&vt&&(Te>.002||De)&&(oe=tx);let Ki=!1;if(kt&&kt.read&&kt.write&&vt&&oe>0){He.uDt.value=Math.min(Ae,1/30),He.uBrush.value=[_e.x,_e.y,_e.vx*jt,_e.vy*jt],He.uBrushPower.value=Ws,He.uKick.value=De?[De.x,De.y,De.strength,0]:[0,0,0,0],He.tOffset.value=kt.read.textures[0],He.tVelocity.value=kt.read.textures[1],Ce.render({scene:vt,target:kt.write,clear:!1});const Ut=kt.read;kt.read=kt.write,kt.write=Ut,oe-=Ae,Ki=oe>0,Ki||(oe=0,an())}De=null,Ue.uStirred.value=Ki?1:0,Ue.tOffset.value=kt&&kt.read?kt.read.textures[0]:fe,E.clearColor(0,0,0,0),Ce.render({scene:Be,target:xe,clear:!0}),Fe&&Ce.render({scene:Fe.mesh,target:xe,clear:!1}),nt.uLight.value=ce.light?1:0,Ce.render({scene:qt,clear:!1});const Xi=Math.abs(fi-he.power)>.002||J>.002||oe>0||Math.abs(he.velocity)>.01||Math.hypot(Re.vx,Re.vy,Re.x-Vr,Re.y-pr)>.001;j&&(Pt||G<1||Xi)&&(Kt=requestAnimationFrame(ln))},lt=()=>{Kt||!j||!V||(Ft=performance.now(),Kt=requestAnimationFrame(ln))},wt=Oe=>{const ce=Pe.getBoundingClientRect(),Ae=Oe.clientX-ce.left,Pt=Oe.clientY-ce.top;return{x:Ae,y:Pt,inside:Ae>=0&&Pt>=0&&Ae<=ce.width&&Pt<=ce.height}},zt=Oe=>{const ce=wt(Oe);ce.inside&&!H.inside&&(H.fresh=!0),H.x=ce.x,H.y=ce.y,H.inside=ce.inside,ce.inside&&lt()},yn=Oe=>{const ce=Ne.current,Ae=wt(Oe);if(!ce||!ce.interactive||ot||!Ae.inside)return;H.inside||(H.fresh=!0),H.x=Ae.x,H.y=Ae.y,H.inside=!0;const Pt=Math.max(8,tt(ce.size,.1,1.5)*Math.min(ft,at)/2),At=(Ae.x-ft/2)/Pt,Yt=(at/2-Ae.y)/Pt;if(Math.hypot(At,Yt)>1.3)return;const Qt=tt(ce.hoverStrength,0,1);De={x:At,y:Yt,strength:Qt*1.2},J=Math.max(J,Qt);const fr=Math.atan2(Yt,At);Xt(fr+(it()-.5)*.5,1.3),Xt(fr+Math.PI+(it()-.5)*1.2,1.1),lt()},un=()=>{H.inside=!1,lt()},Dn=Oe=>{Oe.relatedTarget||un()},St=Oe=>{Oe.pointerType==="touch"&&un()},Gn=()=>{document.hidden||lt()};window.addEventListener("pointermove",zt,{passive:!0}),window.addEventListener("pointerdown",yn,{passive:!0}),window.addEventListener("pointerout",Dn,{passive:!0}),window.addEventListener("pointerup",St,{passive:!0}),window.addEventListener("blur",un),document.addEventListener("visibilitychange",Gn);const dr=new ResizeObserver(yt);dr.observe(Pe);const hr=new IntersectionObserver(([Oe])=>{j=Oe.isIntersecting,lt()});return hr.observe(Pe),we.current=lt,yt(),()=>{var Oe;V=!1,j=!1,cancelAnimationFrame(Kt),dr.disconnect(),hr.disconnect(),window.removeEventListener("pointermove",zt),window.removeEventListener("pointerdown",yn),window.removeEventListener("pointerout",Dn),window.removeEventListener("pointerup",St),window.removeEventListener("blur",un),document.removeEventListener("visibilitychange",Gn),we.current=null,Ot(),Mn(xe),(Oe=E.getExtension("WEBGL_lose_context"))==null||Oe.loseContext(),ee.parentNode&&ee.parentNode.removeChild(ee)}},[]),g.jsx("div",{ref:w,className:`crystalized-ball ${pe}`.trim(),style:de})};function px({onClick:i,disabled:e,label:r="Sign up with Google"}){return g.jsxs("button",{type:"button",className:"google-auth-btn",onClick:i,disabled:e,"aria-label":r,children:[g.jsxs("svg",{className:"google-icon",viewBox:"0 0 24 24",width:"18",height:"18",xmlns:"http://www.w3.org/2000/svg",children:[g.jsx("path",{d:"M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z",fill:"#4285F4"}),g.jsx("path",{d:"M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z",fill:"#34A853"}),g.jsx("path",{d:"M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z",fill:"#FBBC05"}),g.jsx("path",{d:"M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z",fill:"#EA4335"})]}),g.jsx("span",{children:r})]})}function mx({mode:i,setMode:e,onSubmit:r,onGoogleSignIn:o,onForgotPassword:l,loading:c,error:h,resetSent:m}){const[f,v]=ne.useState(""),[x,S]=ne.useState(""),[T,R]=ne.useState(""),[P,b]=ne.useState(!1),[A,F]=ne.useState({}),se=()=>{const W={};return i==="signup"&&!f.trim()&&(W.name="Full name is required"),x.trim()?/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(x.trim())||(W.email="Please enter a valid email address"):W.email="Email address is required",T?T.length<8&&(W.password="Password must be at least 8 characters"):W.password="Password is required",F(W),Object.keys(W).length===0},q=W=>{W.preventDefault(),se()&&r({name:f.trim(),email:x.trim(),password:T})},B=i==="signup";return g.jsxs("div",{className:"auth-form-wrapper",children:[g.jsxs("div",{className:"auth-header",children:[g.jsx("span",{className:"auth-kicker",children:B?"Sign up for free!":"Welcome back!"}),g.jsx("h1",{className:"auth-heading",children:B?"Join Nexora AI":"Welcome back to Nexora AI"})]}),h&&g.jsx("div",{className:"auth-error-banner",role:"alert","aria-live":"assertive",children:g.jsx("span",{children:h})}),m&&g.jsx("div",{className:"auth-success-banner",role:"status","aria-live":"polite",children:"Password reset link sent! Check your inbox."}),g.jsx(px,{onClick:o,disabled:c,label:B?"Sign up with Google":"Log in with Google"}),g.jsxs("div",{className:"auth-divider",children:[g.jsx("div",{className:"auth-divider-line"}),g.jsx("span",{className:"auth-divider-text",children:"OR"}),g.jsx("div",{className:"auth-divider-line"})]}),g.jsxs("form",{className:"auth-fields",onSubmit:q,noValidate:!0,children:[B&&g.jsxs("div",{className:"form-group",children:[g.jsx("label",{htmlFor:"auth-name",className:"visually-hidden",children:"Full Name"}),g.jsx("input",{id:"auth-name",type:"text",className:`auth-input ${A.name?"input-error":""}`,placeholder:"Full name",value:f,onChange:W=>{v(W.target.value),A.name&&F({...A,name:null})},autoComplete:"name",disabled:c}),A.name&&g.jsx("span",{className:"field-error-message",role:"alert",children:A.name})]}),g.jsxs("div",{className:"form-group",children:[g.jsx("label",{htmlFor:"auth-email",className:"visually-hidden",children:"Email"}),g.jsx("input",{id:"auth-email",type:"email",className:`auth-input ${A.email?"input-error":""}`,placeholder:"Email",value:x,onChange:W=>{S(W.target.value),A.email&&F({...A,email:null})},autoComplete:"email",disabled:c}),A.email&&g.jsx("span",{className:"field-error-message",role:"alert",children:A.email})]}),g.jsxs("div",{className:"form-group",children:[g.jsx("label",{htmlFor:"auth-password",className:"visually-hidden",children:"Password"}),g.jsxs("div",{className:"password-input-wrapper",children:[g.jsx("input",{id:"auth-password",type:P?"text":"password",className:`auth-input ${A.password?"input-error":""}`,placeholder:"Password",value:T,onChange:W=>{R(W.target.value),A.password&&F({...A,password:null})},autoComplete:B?"new-password":"current-password",disabled:c}),g.jsx("button",{type:"button",className:"password-toggle-btn",onClick:()=>b(!P),"aria-label":P?"Hide password":"Show password",tabIndex:0,children:P?g.jsx(y0,{size:16}):g.jsx(w0,{size:16})})]}),A.password&&g.jsx("span",{className:"field-error-message",role:"alert",children:A.password}),!B&&g.jsx("div",{className:"forgot-password-row",children:g.jsx("button",{type:"button",className:"forgot-password-link",onClick:()=>l(x),disabled:c,children:"Forgot password?"})})]}),g.jsx("button",{type:"submit",className:"auth-primary-submit-btn",disabled:c,children:c?g.jsx(x0,{size:18,className:"auth-spinner"}):g.jsxs(g.Fragment,{children:[g.jsx("span",{children:B?"Start Chatting":"Log in"}),g.jsx(g0,{size:17,strokeWidth:2.5})]})})]}),g.jsx("div",{className:"auth-mode-switch",children:B?g.jsxs("span",{children:["Already have an account?"," ",g.jsx("button",{type:"button",className:"auth-toggle-link",onClick:()=>e("login"),children:"Log in"})]}):g.jsxs("span",{children:["New here?"," ",g.jsx("button",{type:"button",className:"auth-toggle-link",onClick:()=>e("signup"),children:"Sign up"})]})}),g.jsxs("p",{className:"auth-terms-footer",children:["By continuing, you agree to our"," ",g.jsx("a",{href:"#terms",onClick:W=>W.preventDefault(),children:"Terms"})," and"," ",g.jsx("a",{href:"#privacy",onClick:W=>W.preventDefault(),children:"Privacy Policy"})]})]})}function gx({onAuthenticated:i}){const[e,r]=ne.useState("signup"),[o,l]=ne.useState(!1),[c,h]=ne.useState(""),[m,f]=ne.useState(!1),{loginWithEmail:v,signupWithEmail:x,loginWithGoogle:S,resetPassword:T}=am(),R=async({name:A,email:F,password:se})=>{h(""),f(!1),l(!0);try{e==="signup"?await x(A,F,se):await v(F,se),i&&i()}catch(q){console.error("Auth error:",q);let B=q.message||"Authentication failed. Please check your credentials.";q.code==="auth/wrong-password"||q.code==="auth/invalid-credential"?B="Incorrect email or password. Please try again.":q.code==="auth/email-already-in-use"?B="An account with this email already exists. Please log in.":q.code==="auth/weak-password"?B="Password is too weak. Please use at least 8 characters.":q.code==="auth/popup-closed-by-user"&&(B="Google sign-in popup was closed before completion."),h(B)}finally{l(!1)}},P=async()=>{h(""),f(!1),l(!0);try{await S(),i&&i()}catch(A){console.error("Google sign in error:",A);let F="Google sign-in failed. Please try again.";A.code==="auth/popup-closed-by-user"&&(F="Sign-in popup closed before completion."),h(F)}finally{l(!1)}},b=async A=>{if(!A||!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(A)){h("Please enter your email above first to reset password.");return}h(""),l(!0);try{await T(A),f(!0)}catch(F){h(F.message||"Failed to send password reset email.")}finally{l(!1)}};return g.jsx("div",{className:"auth-viewport",children:g.jsxs("div",{className:"auth-card",children:[g.jsxs("div",{className:"auth-left-panel",children:[g.jsx("div",{className:"auth-brand-wordmark",children:g.jsx("span",{children:"Nexora AI"})}),g.jsxs("div",{className:"ball-interactive-wrapper",children:[g.jsx(fx,{preset:"nebula",color:"#4F8CFF",size:.72,crackle:.85,fill:.5,interactive:!0,hoverStrength:.75}),g.jsx("div",{className:"ball-text-overlay",children:g.jsx("span",{children:"Nexora AI"})})]})]}),g.jsx("div",{className:"auth-right-panel",children:g.jsx("div",{className:"auth-panel-inner",children:g.jsx(mx,{mode:e,setMode:r,onSubmit:R,onGoogleSignIn:P,onForgotPassword:b,loading:o,error:c,resetSent:m})})})]})})}const vx=`#version 300 es
in vec2 aPosition;
uniform vec2 uTexel;
out vec2 vUv;
out vec2 vL;
out vec2 vR;
out vec2 vT;
out vec2 vB;
void main() {
  vUv = aPosition * 0.5 + 0.5;
  vL = vUv - vec2(uTexel.x, 0.0);
  vR = vUv + vec2(uTexel.x, 0.0);
  vT = vUv + vec2(0.0, uTexel.y);
  vB = vUv - vec2(0.0, uTexel.y);
  gl_Position = vec4(aPosition, 0.0, 1.0);
}`,An=`#version 300 es
precision highp float;
precision highp sampler2D;
in vec2 vUv;
in vec2 vL;
in vec2 vR;
in vec2 vT;
in vec2 vB;
out vec4 outColor;
`,yx=`${An}
uniform sampler2D uTarget;
uniform float uAspect;
uniform vec2 uA;
uniform vec2 uB;
uniform float uRadius;
uniform float uWide;
uniform vec3 uValue;
uniform float uMode;
uniform float uStrength;
float erf(float x) {
  float x2 = x * x;
  float a = 0.147;
  return sign(x) * sqrt(1.0 - exp(-x2 * (1.2732395 + a * x2) / (1.0 + a * x2)));
}
float sweep(float along, float length, float across, float radius) {
  return exp(-across * across / (radius * radius)) * 0.5 * (erf(along / radius) - erf((along - length) / radius));
}
void main() {
  vec2 p = vec2(vUv.x * uAspect, vUv.y);
  vec2 a = vec2(uA.x * uAspect, uA.y);
  vec2 ab = vec2(uB.x * uAspect, uB.y) - a;
  float len = length(ab);
  vec2 dir = len > 1e-6 ? ab / len : vec2(1.0, 0.0);
  vec2 ap = p - a;
  vec3 base = texture(uTarget, vUv).xyz;
  if (uMode > 1.5) {
    float along = dot(ap, dir);
    float across = dot(ap, vec2(-dir.y, dir.x));
    if (uMode > 2.5) {
      outColor = vec4(mix(base, uValue, sweep(along, len, across, uRadius) * uStrength), 1.0);
      return;
    }
    vec3 add = vec3(uValue.xy * sweep(along, len, across, uRadius), uValue.z * sweep(along, len, across, uWide));
    outColor = vec4(base + add, 1.0);
    return;
  }
  float h = clamp(dot(ap, ab) / max(dot(ab, ab), 1e-9), 0.0, 1.0);
  vec2 d = ap - ab * h;
  float r2 = dot(d, d);
  float falloff = exp(-r2 / (uRadius * uRadius));
  float wide = exp(-r2 / (uWide * uWide));
  vec3 result = uMode > 0.5 ? mix(base, uValue, falloff * uStrength) : base + vec3(uValue.xy * falloff, uValue.z * wide);
  outColor = vec4(result, 1.0);
}`,wx=`${An}
uniform sampler2D uVelocity;
uniform sampler2D uSource;
uniform vec2 uVelocityTexel;
uniform float uDt;
uniform vec4 uDecay;
void main() {
  vec2 coord = vUv - uDt * texture(uVelocity, vUv).xy * uVelocityTexel;
  outColor = texture(uSource, coord) * uDecay;
}`,xx=`${An}
uniform sampler2D uVelocity;
uniform sampler2D uSource;
uniform sampler2D uForward;
uniform sampler2D uBack;
uniform vec2 uVelocityTexel;
uniform vec2 uSourceTexel;
uniform float uDt;
uniform vec4 uDecay;
void main() {
  vec2 coord = vUv - uDt * texture(uVelocity, vUv).xy * uVelocityTexel;
  vec4 forward = texture(uForward, vUv);
  vec4 corrected = forward + 0.5 * (texture(uSource, vUv) - texture(uBack, vUv));
  vec2 base = (floor(coord / uSourceTexel - 0.5) + 0.5) * uSourceTexel;
  vec4 a = texture(uSource, base);
  vec4 b = texture(uSource, base + vec2(uSourceTexel.x, 0.0));
  vec4 c = texture(uSource, base + vec2(0.0, uSourceTexel.y));
  vec4 d = texture(uSource, base + uSourceTexel);
  vec4 low = min(min(a, b), min(c, d));
  vec4 high = max(max(a, b), max(c, d));
  outColor = clamp(corrected, low, high) * uDecay;
}`,_x=`${An}
uniform sampler2D uVelocity;
void main() {
  float left = texture(uVelocity, vL).x;
  float right = texture(uVelocity, vR).x;
  float top = texture(uVelocity, vT).y;
  float bottom = texture(uVelocity, vB).y;
  vec2 center = texture(uVelocity, vUv).xy;
  if (vL.x < 0.0) left = -center.x;
  if (vR.x > 1.0) right = -center.x;
  if (vT.y > 1.0) top = -center.y;
  if (vB.y < 0.0) bottom = -center.y;
  outColor = vec4(0.5 * (right - left + top - bottom), 0.0, 0.0, 1.0);
}`,Ex=`${An}
uniform sampler2D uSource;
uniform float uValue;
void main() {
  outColor = texture(uSource, vUv) * uValue;
}`,Sx=`${An}
uniform sampler2D uPressure;
uniform sampler2D uDivergence;
void main() {
  float left = texture(uPressure, vL).x;
  float right = texture(uPressure, vR).x;
  float top = texture(uPressure, vT).x;
  float bottom = texture(uPressure, vB).x;
  float divergence = texture(uDivergence, vUv).x;
  outColor = vec4((left + right + bottom + top - divergence) * 0.25, 0.0, 0.0, 1.0);
}`,kx=`${An}
uniform sampler2D uPressure;
uniform sampler2D uVelocity;
void main() {
  float left = texture(uPressure, vL).x;
  float right = texture(uPressure, vR).x;
  float top = texture(uPressure, vT).x;
  float bottom = texture(uPressure, vB).x;
  vec2 velocity = texture(uVelocity, vUv).xy - vec2(right - left, top - bottom);
  outColor = vec4(velocity, 0.0, 1.0);
}`,mm=`
uniform vec3 uColor;
uniform vec3 uSecondary;
uniform float uIntensity;
uniform float uHotspot;
vec3 shade(vec3 dye) {
  float energy = max(dye.x, 0.0);
  float heat = clamp(dye.y, 0.0, energy);
  float gas = max(dye.z, 0.0);
  float fresh = heat / max(energy, 0.0001);
  vec3 tint = mix(uSecondary, uColor, fresh);
  return (tint * energy + uSecondary * gas + vec3(heat * heat * 0.3 * uHotspot)) * uIntensity;
}
`,Tx=`${An}${mm}
uniform sampler2D uDye;
uniform vec2 uDyeTexel;
void main() {
  vec2 o = uDyeTexel * 0.5;
  vec3 light = shade(texture(uDye, vUv + vec2(-o.x, -o.y)).xyz);
  light += shade(texture(uDye, vUv + vec2(o.x, -o.y)).xyz);
  light += shade(texture(uDye, vUv + vec2(-o.x, o.y)).xyz);
  light += shade(texture(uDye, vUv + vec2(o.x, o.y)).xyz);
  outColor = vec4(light * 0.25, 1.0);
}`,Cx=`${An}
uniform sampler2D uSource;
uniform vec2 uSourceTexel;
void main() {
  vec2 o = uSourceTexel;
  vec3 color = texture(uSource, vUv).rgb * 4.0;
  color += texture(uSource, vUv + vec2(-o.x, -o.y)).rgb;
  color += texture(uSource, vUv + vec2(o.x, -o.y)).rgb;
  color += texture(uSource, vUv + vec2(-o.x, o.y)).rgb;
  color += texture(uSource, vUv + vec2(o.x, o.y)).rgb;
  outColor = vec4(color / 8.0, 1.0);
}`,Ix=`${An}
uniform sampler2D uSource;
uniform vec2 uSourceTexel;
void main() {
  vec2 o = uSourceTexel;
  vec3 color = texture(uSource, vUv + vec2(-o.x * 2.0, 0.0)).rgb;
  color += texture(uSource, vUv + vec2(o.x * 2.0, 0.0)).rgb;
  color += texture(uSource, vUv + vec2(0.0, -o.y * 2.0)).rgb;
  color += texture(uSource, vUv + vec2(0.0, o.y * 2.0)).rgb;
  color += texture(uSource, vUv + vec2(-o.x, -o.y)).rgb * 2.0;
  color += texture(uSource, vUv + vec2(o.x, -o.y)).rgb * 2.0;
  color += texture(uSource, vUv + vec2(-o.x, o.y)).rgb * 2.0;
  color += texture(uSource, vUv + vec2(o.x, o.y)).rgb * 2.0;
  outColor = vec4(color / 12.0, 1.0);
}`,Rx=`${An}${mm}
uniform sampler2D uDye;
uniform sampler2D uBloom;
uniform float uGlow;
uniform float uGrain;
uniform float uTime;
uniform float uLight;
float hash(vec2 p) {
  p = fract(p * vec2(123.34, 456.21));
  p += dot(p, p + 45.32);
  return fract(p.x * p.y);
}
void main() {
  vec3 dye = texture(uDye, vUv).xyz;
  vec3 light = shade(dye);
  vec3 bloom = texture(uBloom, vUv).rgb * uGlow;
  float edge = smoothstep(0.0, 0.02, min(min(vUv.x, 1.0 - vUv.x), min(vUv.y, 1.0 - vUv.y)));
  float grain = 1.0 + (hash(gl_FragCoord.xy + fract(uTime * 13.7) * 97.0) - 0.5) * uGrain * 2.0;
  if (uLight > 0.5) {
    float energy = max(dye.x, 0.0);
    float heat = clamp(dye.y, 0.0, energy);
    float gas = max(dye.z, 0.0);
    float fresh = heat / max(energy, 0.0001);
    vec3 tint = mix(uSecondary, uColor, fresh);
    float halo = dot(bloom, vec3(0.2126, 0.7152, 0.0722));
    float density = 1.0 - exp(-((energy * 1.1 + gas * 0.8) * uIntensity + halo * 0.25));
    float tone = dot(tint, vec3(0.2126, 0.7152, 0.0722));
    vec3 ink = tint * min(1.0, 0.5 / max(tone, 0.001)) * mix(0.95, 0.72, smoothstep(0.5, 3.0, energy));
    ink = mix(ink, vec3(1.0), clamp(heat * heat * 0.05 * uHotspot, 0.0, 0.45));
    density = clamp(density * grain, 0.0, 1.0) * edge;
    outColor = vec4(ink * density, density);
  } else {
    vec3 color = 1.0 - exp(-(light + bloom) * grain);
    color *= edge;
    outColor = vec4(color, max(color.r, max(color.g, color.b)));
  }
}`,Df={low:{sim:96,dye:384},medium:{sim:128,dye:576},high:{sim:160,dye:768}},Nx=20,Px=.75,bf=5,_u=(i,e,r)=>Math.min(r,Math.max(e,i)),Lf=(i,e,r)=>{const o=i.createShader(e);return o?(i.shaderSource(o,r),i.compileShader(o),i.getShaderParameter(o,i.COMPILE_STATUS)?o:(i.deleteShader(o),null)):null},Ax=([i,e,r])=>{const o=Math.max(i,e,r),l=Math.min(i,e,r),c=o-l;let h=0;return c>0&&(o===i?h=(e-r)/c%6:o===e?h=(r-i)/c+2:h=(i-e)/c+4),[(h*60+360)%360,o>0?c/o:0,o]},Mx=(i,e,r)=>{const o=(i%360+360)%360/60,l=r*e,c=l*(1-Math.abs(o%2-1)),h=r-l,[m,f,v]=o<1?[l,c,0]:o<2?[c,l,0]:o<3?[0,l,c]:o<4?[0,c,l]:o<5?[c,0,l]:[l,0,c];return[m+h,f+h,v+h]},Dx=({color:i="#5f8bff",secondaryColor:e,intensity:r=1.3,trailWidth:o=3,linger:l=1.4,glow:c=1.2,hotspot:h=.8,followSpeed:m=.6,grain:f=0,clickBurst:v=!0,quality:x="high",theme:S="dark",blendMode:T,maxDevicePixelRatio:R=2,enabled:P=!0,children:b,className:A="",style:F,...se})=>{const q=ne.useRef(null),B=ne.useRef(null),W=ne.useRef(null);W.current={color:String(i),secondaryColor:e?String(e):"",intensity:Math.max(0,r),trailWidth:_u(o,.5,40),linger:_u(l,.1,10),glow:Math.max(0,c),hotspot:Math.max(0,h),followSpeed:_u(m,0,1),grain:Math.max(0,f),clickBurst:v,quality:Df[x]?x:"high",theme:S,maxDevicePixelRatio:R,enabled:P},ne.useEffect(()=>{var Et;const pe=q.current,de=B.current,w=de==null?void 0:de.getContext("webgl2",{alpha:!0,premultipliedAlpha:!0,antialias:!1,depth:!1,stencil:!1});if(!pe||!de||!w||!w.getExtension("EXT_color_buffer_float"))return;const Ne=Lf(w,w.VERTEX_SHADER,vx);if(!Ne)return;const we=L=>{const G=Lf(w,w.FRAGMENT_SHADER,L),j=w.createProgram();if(!G||!j)return null;if(w.attachShader(j,Ne),w.attachShader(j,G),w.bindAttribLocation(j,0,"aPosition"),w.linkProgram(j),w.deleteShader(G),!w.getProgramParameter(j,w.LINK_STATUS))return w.deleteProgram(j),null;const V={},J=w.getProgramParameter(j,w.ACTIVE_UNIFORMS);for(let oe=0;oe<J;oe++){const Te=w.getActiveUniform(j,oe);Te&&(V[Te.name]=w.getUniformLocation(j,Te.name))}return{program:j,uniforms:V}},ye={splat:we(yx),advect:we(wx),maccormack:we(xx),divergence:we(_x),scale:we(Ex),pressure:we(Sx),gradient:we(kx),prefilter:we(Tx),down:we(Cx),up:we(Ix),display:we(Rx)};if(Object.values(ye).some(L=>!L))return;const me=w.createVertexArray(),ue=w.createBuffer();w.bindVertexArray(me),w.bindBuffer(w.ARRAY_BUFFER,ue),w.bufferData(w.ARRAY_BUFFER,new Float32Array([-1,-1,3,-1,-1,3]),w.STATIC_DRAW),w.enableVertexAttribArray(0),w.vertexAttribPointer(0,2,w.FLOAT,!1,0,0);const Ve=document.createElement("canvas");Ve.width=1,Ve.height=1;const Pe=Ve.getContext("2d",{willReadFrequently:!0}),Ce=((Et=window.matchMedia)==null?void 0:Et.call(window,"(prefers-reduced-motion: reduce)").matches)??!1,E={width:1,height:1,ratio:1,colorKey:"",color:[.37,.55,1],secondary:[.25,.3,1],pointer:{x:0,y:0,inside:!1},emitter:{x:0,y:0,vx:0,vy:0,px:0,py:0},ready:!1,bursts:[],active:-1/0,time:0,allocated:"",targets:null};let ee=0,Y=0,C=!0,O=!0;const Se=(L,G)=>{if(!Pe||!L)return G;const j=/^[0-9a-f]{3,8}$/i.test(L)?`#${L}`:L;Pe.clearRect(0,0,1,1),Pe.fillStyle="#000000",Pe.fillStyle=j,Pe.fillRect(0,0,1,1);const[V,J,oe]=Pe.getImageData(0,0,1,1).data;return[V/255,J/255,oe/255]},fe=L=>{const G=`${L.color}|${L.secondaryColor}`;if(G!==E.colorKey)if(E.colorKey=G,E.color=Se(L.color,[.37,.55,1]),L.secondaryColor)E.secondary=Se(L.secondaryColor,E.color);else{const[j,V,J]=Ax(E.color);E.secondary=Mx(j+8,Math.min(1,V*1.1+.05),J)}},ke=(L,G,j,V,J)=>{const oe=w.createTexture();w.bindTexture(w.TEXTURE_2D,oe),w.texParameteri(w.TEXTURE_2D,w.TEXTURE_MIN_FILTER,J),w.texParameteri(w.TEXTURE_2D,w.TEXTURE_MAG_FILTER,J),w.texParameteri(w.TEXTURE_2D,w.TEXTURE_WRAP_S,w.CLAMP_TO_EDGE),w.texParameteri(w.TEXTURE_2D,w.TEXTURE_WRAP_T,w.CLAMP_TO_EDGE),w.texImage2D(w.TEXTURE_2D,0,j,L,G,0,V,w.HALF_FLOAT,null);const Te=w.createFramebuffer();return w.bindFramebuffer(w.FRAMEBUFFER,Te),w.framebufferTexture2D(w.FRAMEBUFFER,w.COLOR_ATTACHMENT0,w.TEXTURE_2D,oe,0),w.viewport(0,0,L,G),w.clearColor(0,0,0,0),w.clear(w.COLOR_BUFFER_BIT),{texture:oe,fbo:Te,width:L,height:G,texel:[1/L,1/G]}},xe=(L,G,j,V,J)=>{let oe=ke(L,G,j,V,J),Te=ke(L,G,j,V,J);return{get read(){return oe},get write(){return Te},swap(){const De=oe;oe=Te,Te=De},targets(){return[oe,Te]}}},Me=L=>{w.deleteTexture(L.texture),w.deleteFramebuffer(L.fbo)},te=()=>{const L=E.targets;L&&([...L.velocity.targets(),...L.dye.targets(),...L.pressure.targets(),L.divergence,L.forward,L.back,...L.bloom].forEach(Me),E.targets=null)},Le=()=>{const L=E.targets;L&&(w.clearColor(0,0,0,0),[...L.velocity.targets(),...L.dye.targets(),...L.pressure.targets()].forEach(G=>{w.bindFramebuffer(w.FRAMEBUFFER,G.fbo),w.clear(w.COLOR_BUFFER_BIT)}))},Ue=()=>{const L=W.current,G=`${L.quality}|${E.width}|${E.height}|${de.width}|${de.height}`;if(G===E.allocated&&E.targets)return;te(),E.allocated=G;const j=Df[L.quality],V=E.width/E.height,J=Re=>V>=1?[Math.round(Re*V),Re]:[Re,Math.round(Re/V)],[oe,Te]=J(j.sim);let[De,D]=J(j.dye);const K=Math.min(1,de.width/De,de.height/D);De=Math.max(2,Math.round(De*K)),D=Math.max(2,Math.round(D*K));const H=[];let he=De>>1,_e=D>>1;for(let Re=0;Re<bf;Re++)H.push(ke(Math.max(1,he),Math.max(1,_e),w.RGBA16F,w.RGBA,w.LINEAR)),he>>=1,_e>>=1;E.targets={velocity:xe(oe,Te,w.RG16F,w.RG,w.LINEAR),dye:xe(De,D,w.RGBA16F,w.RGBA,w.LINEAR),forward:ke(De,D,w.RGBA16F,w.RGBA,w.LINEAR),back:ke(De,D,w.RGBA16F,w.RGBA,w.LINEAR),pressure:xe(oe,Te,w.R16F,w.RED,w.NEAREST),divergence:ke(oe,Te,w.R16F,w.RED,w.NEAREST),bloom:H}},He=()=>{const L=W.current,G=Math.max(1,pe.clientWidth),j=Math.max(1,pe.clientHeight),V=Math.min(window.devicePixelRatio||1,Math.max(.5,L.maxDevicePixelRatio||2)),J=Math.max(1,Math.round(G*V)),oe=Math.max(1,Math.round(j*V));(de.width!==J||de.height!==oe)&&(de.width=J,de.height=oe),E.width=G,E.height=j,E.ratio=V,Ue()},nt=L=>{L?(w.bindFramebuffer(w.FRAMEBUFFER,L.fbo),w.viewport(0,0,L.width,L.height)):(w.bindFramebuffer(w.FRAMEBUFFER,null),w.viewport(0,0,de.width,de.height)),w.drawArrays(w.TRIANGLES,0,3)},Qe=(L,G)=>(w.useProgram(L.program),L.uniforms.uTexel&&w.uniform2f(L.uniforms.uTexel,G[0],G[1]),L.uniforms),Be=(L,G)=>(w.activeTexture(w.TEXTURE0+L),w.bindTexture(w.TEXTURE_2D,G.texture),L),sn=(L,G,j,V,J,oe,Te,De,D,K=oe)=>{const H=Qe(ye.splat,L.read.texel);w.uniform1i(H.uTarget,Be(0,L.read)),w.uniform1f(H.uAspect,E.width/E.height),w.uniform2f(H.uA,G/E.width,1-j/E.height),w.uniform2f(H.uB,V/E.width,1-J/E.height),w.uniform1f(H.uRadius,oe/E.height),w.uniform1f(H.uWide,K/E.height),w.uniform3f(H.uValue,Te[0],Te[1],Te[2]),w.uniform1f(H.uMode,De),w.uniform1f(H.uStrength,D),nt(L.write),L.swap()},vt=(L,G)=>{const{velocity:j}=E.targets;return[L*j.read.width/E.width,-G*j.read.height/E.height]},qt=L=>Math.max(L.trailWidth*.5,E.height/E.targets.dye.read.height*.9),Mn=(L,G,j)=>{const{emitter:V,pointer:J}=E,{velocity:oe,dye:Te}=E.targets;if(V.px=V.x,V.py=V.y,Ce||L.followSpeed>=1)V.x=J.x,V.y=J.y;else{const he=10+L.followSpeed*50,_e=Math.max(1,Math.ceil(G/.004)),Re=G/_e;for(let yt=0;yt<_e;yt++)V.vx+=(he*he*(J.x-V.x)-2*he*V.vx)*Re,V.vy+=(he*he*(J.y-V.y)-2*he*V.vy)*Re,V.x+=V.vx*Re,V.y+=V.vy*Re}const De=V.x-V.px,D=V.y-V.py;if(Math.hypot(De,D)<.05||!L.enabled)return;const H=qt(L);if(!Ce){const he=vt(De/Math.max(G,.001),D/Math.max(G,.001));sn(oe,V.px,V.py,V.x,V.y,H*4+18,[he[0],he[1],0],3,Px*.6)}sn(Te,V.px,V.py,V.x,V.y,H,[5.6,5.6,.7],2,1,H*5+6),E.active=j},Hn=(L,G,j,V)=>{const{velocity:J,dye:oe}=E.targets,Te=qt(L),De=6,D=Math.random()*Math.PI*2;for(let K=0;K<De;K++){const H=D+K/De*Math.PI*2+(Math.random()-.5)*.5,he=Math.cos(H),_e=Math.sin(H),Re=20+Math.random()*14,yt=G+he*3,Xt=j+_e*3,ln=G+he*Re,lt=j+_e*Re;if(!Ce){const wt=vt(Math.cos(H+.6)*760,Math.sin(H+.6)*760);sn(J,yt,Xt,ln,lt,18,[wt[0],wt[1],0],1,.9)}sn(oe,yt,Xt,ln,lt,Te*1.1,[2.4,2.4,.3],0,1,Te*5+6)}sn(oe,G,j,G+.01,j,Te*2.2,[1.8,1.8,.4],0,1,Te*7+10),E.active=V},on=(L,G)=>{const{velocity:j,dye:V,pressure:J,divergence:oe}=E.targets;if(!Ce){let H=Qe(ye.divergence,j.read.texel);w.uniform1i(H.uVelocity,Be(0,j.read)),nt(oe),H=Qe(ye.scale,J.read.texel),w.uniform1i(H.uSource,Be(0,J.read)),w.uniform1f(H.uValue,.8),nt(J.write),J.swap(),H=Qe(ye.pressure,J.read.texel),w.uniform1i(H.uDivergence,Be(1,oe));for(let _e=0;_e<Nx;_e++)w.uniform1i(H.uPressure,Be(0,J.read)),nt(J.write),J.swap();H=Qe(ye.gradient,j.read.texel),w.uniform1i(H.uPressure,Be(0,J.read)),w.uniform1i(H.uVelocity,Be(1,j.read)),nt(j.write),j.swap(),H=Qe(ye.advect,j.read.texel),w.uniform2f(H.uVelocityTexel,j.read.texel[0],j.read.texel[1]),w.uniform1i(H.uVelocity,Be(0,j.read)),w.uniform1i(H.uSource,Be(0,j.read)),w.uniform1f(H.uDt,G);const he=Math.exp(-G*1.2);w.uniform4f(H.uDecay,he,he,1,1),nt(j.write),j.swap()}const Te=[Math.exp(-G*4.6/(L.linger*.8)),Math.exp(-G*4.6/(L.linger*.2)),Math.exp(-G*4.6/(L.linger*1.2)),1],{forward:De,back:D}=E.targets;if(Ce){const H=Qe(ye.advect,V.read.texel);w.uniform2f(H.uVelocityTexel,j.read.texel[0],j.read.texel[1]),w.uniform1i(H.uVelocity,Be(0,j.read)),w.uniform1i(H.uSource,Be(1,V.read)),w.uniform1f(H.uDt,0),w.uniform4f(H.uDecay,Te[0],Te[1],Te[2],Te[3]),nt(V.write),V.swap();return}let K=Qe(ye.advect,V.read.texel);w.uniform2f(K.uVelocityTexel,j.read.texel[0],j.read.texel[1]),w.uniform1i(K.uVelocity,Be(0,j.read)),w.uniform1i(K.uSource,Be(1,V.read)),w.uniform1f(K.uDt,G),w.uniform4f(K.uDecay,1,1,1,1),nt(De),w.uniform1i(K.uSource,Be(1,De)),w.uniform1f(K.uDt,-G),nt(D),K=Qe(ye.maccormack,V.read.texel),w.uniform2f(K.uVelocityTexel,j.read.texel[0],j.read.texel[1]),w.uniform2f(K.uSourceTexel,V.read.texel[0],V.read.texel[1]),w.uniform1i(K.uVelocity,Be(0,j.read)),w.uniform1i(K.uSource,Be(1,V.read)),w.uniform1i(K.uForward,Be(2,De)),w.uniform1i(K.uBack,Be(3,D)),w.uniform1f(K.uDt,G),w.uniform4f(K.uDecay,Te[0],Te[1],Te[2],Te[3]),nt(V.write),V.swap()},Fe=(L,G)=>{w.uniform3f(L.uColor,E.color[0],E.color[1],E.color[2]),w.uniform3f(L.uSecondary,E.secondary[0],E.secondary[1],E.secondary[2]),w.uniform1f(L.uIntensity,G.intensity),w.uniform1f(L.uHotspot,G.hotspot)},Ot=L=>{const{dye:G,bloom:j}=E.targets;if(L.glow>0){let J=Qe(ye.prefilter,j[0].texel);w.uniform1i(J.uDye,Be(0,G.read)),w.uniform2f(J.uDyeTexel,G.read.texel[0],G.read.texel[1]),Fe(J,L),nt(j[0]),J=Qe(ye.down,j[0].texel);for(let oe=1;oe<j.length;oe++)w.uniform1i(J.uSource,Be(0,j[oe-1])),w.uniform2f(J.uSourceTexel,j[oe-1].texel[0],j[oe-1].texel[1]),nt(j[oe]);w.enable(w.BLEND),w.blendFunc(w.ONE,w.ONE),J=Qe(ye.up,j[0].texel);for(let oe=j.length-1;oe>0;oe--)w.uniform1i(J.uSource,Be(0,j[oe])),w.uniform2f(J.uSourceTexel,j[oe].texel[0],j[oe].texel[1]),nt(j[oe-1]);w.disable(w.BLEND)}const V=Qe(ye.display,[1/de.width,1/de.height]);w.uniform1i(V.uDye,Be(0,G.read)),w.uniform1i(V.uBloom,Be(1,j[0])),Fe(V,L),w.uniform1f(V.uGlow,L.glow>0?L.glow*1.4/bf:0),w.uniform1f(V.uGrain,L.grain),w.uniform1f(V.uTime,E.time),w.uniform1f(V.uLight,L.theme==="light"?1:0),nt(null)},an=()=>{w.bindFramebuffer(w.FRAMEBUFFER,null),w.viewport(0,0,de.width,de.height),w.clearColor(0,0,0,0),w.clear(w.COLOR_BUFFER_BIT)},Wn=L=>{if(ee=0,!C||!O||document.hidden)return;const G=W.current,j=Y?Math.min(1/30,(L-Y)/1e3):1/60;Y=L,E.time+=j;const V=Math.min(window.devicePixelRatio||1,Math.max(.5,G.maxDevicePixelRatio||2));for(Math.abs(V-E.ratio)>.01&&He(),Ue(),fe(G),w.bindVertexArray(me),w.disable(w.BLEND),E.ready&&Mn(G,j,L);E.bursts.length;){const[Te,De]=E.bursts.shift();Hn(G,Te,De,L)}on(G,j),Ot(G);const J=L-E.active>G.linger*1200+900,oe=Math.hypot(E.emitter.vx,E.emitter.vy)<1;if(J&&oe){Le(),an(),Y=0;return}ee=requestAnimationFrame(Wn)},ot=()=>{!ee&&C&&O&&!document.hidden&&(ee=requestAnimationFrame(Wn))},it=L=>{const G=pe.getBoundingClientRect(),j=L.clientX-G.left,V=L.clientY-G.top;if(!(j>=0&&V>=0&&j<=G.width&&V<=G.height)){E.pointer.inside&&(E.pointer.inside=!1,E.ready=!1,ot());return}E.ready||(E.emitter.x=j,E.emitter.y=V,E.emitter.px=j,E.emitter.py=V,E.emitter.vx=0,E.emitter.vy=0,E.ready=!0),E.pointer.x=j,E.pointer.y=V,E.pointer.inside=!0,ot()},ft=L=>{const G=W.current;if(!G.clickBurst||!G.enabled)return;const j=pe.getBoundingClientRect(),V=L.clientX-j.left,J=L.clientY-j.top;V<0||J<0||V>j.width||J>j.height||(E.bursts.push([V,J]),ot())},at=()=>{E.pointer.inside=!1,E.ready=!1,ot()},Kt=()=>{Y=0,ot()},Ft=new ResizeObserver(()=>{He(),ot()});Ft.observe(pe);const Nt=new IntersectionObserver(L=>{O=L.some(G=>G.isIntersecting),O&&(Y=0,ot())});return Nt.observe(pe),window.addEventListener("pointermove",it,{passive:!0}),window.addEventListener("pointerdown",ft,{passive:!0}),document.documentElement.addEventListener("pointerleave",at),document.addEventListener("visibilitychange",Kt),He(),an(),()=>{C=!1,cancelAnimationFrame(ee),Ft.disconnect(),Nt.disconnect(),window.removeEventListener("pointermove",it),window.removeEventListener("pointerdown",ft),document.documentElement.removeEventListener("pointerleave",at),document.removeEventListener("visibilitychange",Kt),te(),Object.values(ye).forEach(L=>w.deleteProgram(L.program)),w.deleteShader(Ne),w.deleteBuffer(ue),w.deleteVertexArray(me)}},[]);const Q=T??(S==="light"?"normal":"screen");return g.jsxs("div",{ref:q,className:`glow-cursor${A?` ${A}`:""}`,style:F,...se,children:[g.jsx("canvas",{ref:B,className:"glow-cursor__canvas",style:{mixBlendMode:Q},"aria-hidden":"true"}),b&&g.jsx("div",{className:"glow-cursor__content",children:b})]})};function ta({size:i=64,className:e=""}){return g.jsxs("div",{className:`nexora-orb ${e}`,style:{width:`${i}px`,height:`${i}px`},"aria-hidden":"true",children:[g.jsx("div",{className:"nexora-orb-glow"}),g.jsxs("div",{className:"nexora-orb-sphere",children:[g.jsx("div",{className:"nexora-orb-specular"}),g.jsx("div",{className:"nexora-orb-inner-shadow"}),g.jsx("div",{className:"nexora-orb-core"})]})]})}const bt="http://localhost:8000";function bx(){const{user:i,loading:e,signOut:r}=am(),[o,l]=ne.useState(!1),[c,h]=ne.useState("chat"),[m,f]=ne.useState(!1),[v,x]=ne.useState(""),[S,T]=ne.useState(!1),[R,P]=ne.useState(!1),[b,A]=ne.useState(!1),[F,se]=ne.useState([]),[q,B]=ne.useState(null),[W,Q]=ne.useState(null),[pe,de]=ne.useState(""),[w,Ne]=ne.useState([]),[we,ye]=ne.useState(!1),[me,ue]=ne.useState(null),[Ve,Pe]=ne.useState(.1),[Ce,E]=ne.useState("customer"),[ee,Y]=ne.useState("GLOBAL"),[C,O]=ne.useState(null),[Se,fe]=ne.useState(!1),[ke,xe]=ne.useState(!1),[Me,te]=ne.useState(""),[Le,Ue]=ne.useState(""),[He,nt]=ne.useState(null),[Qe,Be]=ne.useState([]),[sn,vt]=ne.useState(null),[qt,Mn]=ne.useState(""),[Hn,on]=ne.useState(null),Fe=ne.useRef(null),Ot=ne.useRef(null),an=ne.useRef(null);ne.useEffect(()=>{Wn(),ot()},[]),ne.useEffect(()=>{q&&it(q)},[q]),ne.useEffect(()=>{c==="dashboard"?ft():c==="tickets"&&at()},[c]),ne.useEffect(()=>{var D;(D=Fe.current)==null||D.scrollIntoView({behavior:"smooth"})},[W==null?void 0:W.messages,we]),ne.useEffect(()=>{function D(K){an.current&&!an.current.contains(K.target)&&P(!1)}return document.addEventListener("mousedown",D),()=>document.removeEventListener("mousedown",D)},[]);const Wn=async()=>{try{const K=await(await fetch(`${bt}/api/config`)).json();ue(K)}catch(D){console.error("Failed to load config",D)}},ot=async()=>{var D;try{const H=await(await fetch(`${bt}/api/chats?show_archived=${S}&search=${encodeURIComponent(v)}`)).json();se(H.chats||[]),!q&&((D=H.chats)==null?void 0:D.length)>0&&B(H.chats[0].id)}catch(K){console.error("Failed to load chats",K)}},it=async D=>{try{const K=await fetch(`${bt}/api/chats/${D}`);if(K.ok){const H=await K.json();Q(H.chat),Ne(H.files||[])}}catch(K){console.error("Failed to load single chat",K)}},ft=async()=>{try{const K=await(await fetch(`${bt}/api/dashboard`)).json();nt(K)}catch(D){console.error("Failed to load dashboard",D)}},at=async()=>{try{const K=await(await fetch(`${bt}/api/tickets`)).json();Be(K.tickets||[])}catch(D){console.error("Failed to load tickets",D)}},Kt=async()=>{try{const K=await(await fetch(`${bt}/api/chats`,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({title:"New Conversation"})})).json();se(H=>[K.chat,...H]),B(K.chat.id),Q(K.chat),Ne([]),h("chat"),l(!1)}catch(D){console.error("Failed to create new chat",D)}},Ft=async D=>{const K=Array.from(D.target.files);if(!(!K.length||!q)){for(const H of K){const he=new FormData;he.append("file",H);try{const Re=await(await fetch(`${bt}/api/chats/${q}/files`,{method:"POST",body:he})).json();Ne(yt=>[...yt,Re.file])}catch(_e){console.error("Error uploading file",_e)}}Ot.current&&(Ot.current.value="")}},Nt=async D=>{if(q)try{await fetch(`${bt}/api/chats/${q}/files/${D}`,{method:"DELETE"}),Ne(K=>K.filter(H=>H.id!==D))}catch(K){console.error("Failed to delete attached file",K)}},Et=async(D=null)=>{const K=(D||pe).trim();if(!K||we)return;let H=q;if(!H){const Re=await(await fetch(`${bt}/api/chats`,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({title:K.slice(0,30)})})).json();se(yt=>[Re.chat,...yt]),H=Re.chat.id,B(H),Q(Re.chat)}const he={role:"user",content:K,timestamp:new Date().toISOString()};Q(_e=>({..._e,messages:[...(_e==null?void 0:_e.messages)||[],he]})),de(""),ye(!0);try{const Re=(await fetch(`${bt}/api/chat`,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({question:K,chat_id:H,temperature:Ve,user_role:Ce,user_region:ee})})).body.getReader(),yt=new TextDecoder("utf-8");let Xt="",ln=null,lt=null;for(Q(wt=>({...wt,messages:[...wt.messages,{role:"assistant",content:"",timestamp:new Date().toISOString(),streaming:!0}]}));;){const{value:wt,done:zt}=await Re.read();if(zt)break;const un=yt.decode(wt,{stream:!0}).split(`

`);for(const Dn of un)if(Dn.startsWith("data: "))try{const St=JSON.parse(Dn.substring(6));St.token&&(Xt+=St.token,Q(Gn=>{const dr=[...Gn.messages],hr=dr[dr.length-1];return hr&&hr.role==="assistant"&&(hr.content=Xt),{...Gn,messages:dr}})),St.escalation&&(ln=St.escalation,on(St.escalation)),St.metadata&&(lt=St.metadata)}catch{}}Q(wt=>{const zt=[...wt.messages],yn=zt[zt.length-1];return yn&&yn.role==="assistant"&&(yn.streaming=!1,ln&&(yn.escalation=ln),lt&&(yn.metadata=lt)),{...wt,messages:zt}}),ot()}catch(_e){console.error("Chat stream failed",_e),Q(Re=>({...Re,messages:[...Re.messages,{role:"assistant",content:"Connection lost or API unavailable. Please check your connection.",isError:!0}]}))}finally{ye(!1)}},L=async(D,K)=>{try{await fetch(`${bt}/api/feedback`,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({chat_id:q,message_index:D,helpful:K})}),Q(H=>{const he=[...H.messages];return he[D]&&(he[D].feedback=K),{...H,messages:he}})}catch(H){console.error("Feedback failed",H)}},G=async D=>{if(qt.trim())try{await fetch(`${bt}/api/chats/${q}/messages/${D}`,{method:"PUT",headers:{"Content-Type":"application/json"},body:JSON.stringify({content:qt})}),vt(null),Et(qt)}catch(K){console.error("Save edit failed",K)}},j=async()=>{if(Me.trim())try{await fetch(`${bt}/api/tickets`,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({chat_id:q,contact:Me,issue_summary:Le||(W==null?void 0:W.title)||"General Customer Inquiry"})}),xe(!1),te(""),Ue(""),at(),alert("Support Ticket Generated and Routed Successfully (Task 3)")}catch(D){console.error("Create ticket failed",D)}},V=(D,K)=>{navigator.clipboard.writeText(D),O(K),setTimeout(()=>O(null),2e3)};if(e)return g.jsx("div",{style:{width:"100vw",height:"100vh",background:"#0a0d13",display:"flex",alignItems:"center",justifyContent:"center"},children:g.jsx("div",{className:"pulse-spinner",style:{width:32,height:32,borderTopColor:"#4fd1c5"}})});if(!i)return g.jsx(gx,{});const J=F.filter(D=>!(!S&&D.archived||v&&!D.title.toLowerCase().includes(v.toLowerCase()))),oe=(W==null?void 0:W.messages)&&W.messages.length>0,Te=i!=null&&i.displayName?i.displayName.split(" ")[0]:"",De=((i==null?void 0:i.displayName)||(i==null?void 0:i.email)||"U").slice(0,2).toUpperCase();return g.jsxs("div",{className:"app-shell",children:[g.jsxs("aside",{className:`app-sidebar ${o?"open":""}`,children:[g.jsxs("div",{className:"sidebar-top",children:[g.jsxs("div",{className:"sidebar-brand-row",children:[g.jsxs("div",{className:"sidebar-brand",onClick:()=>{h("chat"),Q(null),B(null)},children:[g.jsx(ta,{size:26}),g.jsx("span",{className:"brand-text",children:"Nexora AI"})]}),g.jsx("button",{className:"sidebar-icon-btn",title:"Search Chats",onClick:()=>f(!m),"aria-label":"Toggle search",children:g.jsx(S0,{size:16})})]}),m&&g.jsx("div",{className:"sidebar-search-box",children:g.jsx("input",{type:"text",className:"sidebar-search-input",placeholder:"Search chats...",value:v,onChange:D=>x(D.target.value),autoFocus:!0})}),g.jsxs("button",{className:"btn-new-chat-pill",onClick:Kt,children:[g.jsx(Xo,{size:16,style:{color:"var(--accent-teal)"}}),g.jsx("span",{children:"New Chat"})]})]}),g.jsxs("div",{className:"sidebar-section",children:[g.jsx("div",{className:"sidebar-section-title",children:"Features"}),g.jsxs("div",{className:"sidebar-nav-list",children:[g.jsxs("button",{className:`sidebar-nav-item ${c==="chat"?"active":""}`,onClick:()=>{h("chat"),l(!1)},children:[g.jsx(E0,{size:16}),g.jsx("span",{children:"Assistant"})]}),g.jsxs("button",{className:`sidebar-nav-item ${c==="dashboard"?"active":""}`,onClick:()=>{h("dashboard"),l(!1)},children:[g.jsx(Ch,{size:16}),g.jsx("span",{children:"Metrics & Telemetry"})]}),g.jsxs("button",{className:`sidebar-nav-item ${c==="tickets"?"active":""}`,onClick:()=>{h("tickets"),l(!1)},children:[g.jsx(Ko,{size:16}),g.jsx("span",{children:"Support Tickets"})]}),g.jsxs("button",{className:"sidebar-nav-item",onClick:()=>{fe(!0),l(!1)},children:[g.jsx(Mh,{size:16}),g.jsx("span",{children:"Settings & Security"})]})]})]}),g.jsxs("div",{className:"sidebar-section",style:{flex:1,display:"flex",flexDirection:"column",minHeight:0,paddingBottom:0},children:[g.jsx("div",{className:"sidebar-section-title",children:"Your Chats"}),g.jsxs("div",{className:"sidebar-chat-scroll",children:[J.map(D=>g.jsxs("div",{className:`sidebar-chat-item ${D.id===q&&c==="chat"?"active":""}`,onClick:()=>{B(D.id),h("chat"),l(!1)},children:[g.jsxs("div",{className:"sidebar-chat-title",title:D.title,children:[D.pinned&&g.jsx(Ph,{size:11,color:"var(--accent-amber)",style:{marginRight:6,display:"inline"}}),D.title||"Conversation"]}),g.jsxs("div",{className:"sidebar-chat-actions",onClick:K=>K.stopPropagation(),children:[g.jsx("button",{className:"chat-action-btn",title:D.pinned?"Unpin":"Pin",onClick:async()=>{await fetch(`${bt}/api/chats/${D.id}/pin`,{method:"POST"}),ot()},children:g.jsx(Ph,{size:12,color:D.pinned?"var(--accent-amber)":"currentColor"})}),g.jsx("button",{className:"chat-action-btn",title:"Delete",onClick:async()=>{await fetch(`${bt}/api/chats/${D.id}`,{method:"DELETE"}),ot(),q===D.id&&(Q(null),B(null))},children:g.jsx(C0,{size:12})})]})]},D.id)),J.length===0&&g.jsx("div",{style:{padding:"0.75rem",fontSize:"0.78rem",color:"var(--text-muted)",textAlign:"center"},children:"No active conversations"})]})]}),g.jsxs("div",{className:"sidebar-footer",children:[g.jsxs("div",{className:"sidebar-user-info",children:[i!=null&&i.photoURL?g.jsx("img",{src:i.photoURL,alt:"User",className:"sidebar-user-avatar"}):g.jsx("div",{className:"sidebar-user-avatar",children:De}),g.jsxs("div",{className:"sidebar-user-details",children:[g.jsx("span",{className:"sidebar-user-name",children:(i==null?void 0:i.displayName)||(i==null?void 0:i.email)}),g.jsxs("span",{className:"sidebar-user-sub",children:[g.jsx("span",{style:{width:6,height:6,borderRadius:"50%",background:"var(--accent-emerald)",display:"inline-block"}}),"Online"]})]})]}),g.jsx("button",{className:"sidebar-icon-btn",title:"Sign out",onClick:r,style:{color:"var(--accent-rose)"},children:g.jsx(Nh,{size:15})})]})]}),g.jsxs("main",{className:"app-main",children:[g.jsx("div",{className:"ambient-top-glow"}),g.jsxs("header",{className:"main-top-bar",children:[g.jsxs("div",{className:"top-bar-left",children:[g.jsx("button",{className:"mobile-menu-btn",onClick:()=>l(!o),"aria-label":"Toggle navigation drawer",children:g.jsx(_0,{size:18})}),g.jsxs("div",{className:"model-selector-pill",onClick:()=>fe(!0),title:"Click to view & configure RAG model options",children:[g.jsx(Dh,{className:"model-pill-icon"}),g.jsx("span",{children:"Gemini RAG v3.6"}),g.jsx(Ih,{size:13,style:{color:"var(--text-muted)"}})]})]}),g.jsxs("div",{className:"top-bar-right",children:[g.jsxs("nav",{className:"top-nav-links",children:[g.jsx("button",{className:`top-nav-link ${c==="dashboard"?"active":""}`,onClick:()=>h("dashboard"),children:"Dashboard"}),g.jsx("button",{className:"top-nav-link",onClick:()=>fe(!0),children:"Settings"}),g.jsx("button",{className:`top-nav-link ${c==="tickets"?"active":""}`,onClick:()=>h("tickets"),children:"Help & Support"})]}),g.jsxs("div",{className:"user-avatar-wrapper",ref:an,children:[g.jsx("button",{className:"user-avatar-btn",onClick:()=>P(!R),"aria-label":"User profile menu",children:i!=null&&i.photoURL?g.jsx("img",{src:i.photoURL,alt:"Profile",className:"user-avatar-img"}):g.jsx("div",{className:"user-avatar-fallback",children:De})}),R&&g.jsxs("div",{className:"user-menu-dropdown",children:[g.jsxs("div",{className:"user-menu-header",children:[g.jsx("div",{className:"user-menu-name",children:(i==null?void 0:i.displayName)||"Nexora User"}),g.jsx("div",{className:"user-menu-email",children:i==null?void 0:i.email})]}),g.jsxs("button",{className:"user-menu-item",onClick:()=>{fe(!0),P(!1)},children:[g.jsx(Mh,{size:14})," Settings"]}),g.jsxs("button",{className:"user-menu-item",onClick:()=>{xe(!0),P(!1)},children:[g.jsx(Ko,{size:14})," Submit Support Case"]}),g.jsxs("button",{className:"user-menu-item",style:{color:"var(--accent-rose)"},onClick:r,children:[g.jsx(Nh,{size:14})," Sign out"]})]})]})]})]}),c==="chat"&&g.jsx(g.Fragment,{children:oe?g.jsxs("div",{className:"conversation-view",children:[g.jsxs("div",{className:"conversation-scroll",children:[W.messages.map((D,K)=>{const H=D.role==="user",he=sn===K;return g.jsxs("div",{className:`message-row ${H?"user":"assistant"}`,children:[g.jsx("div",{className:"message-sender-avatar",children:H?De:g.jsx(ta,{size:26})}),g.jsxs("div",{className:"message-content-wrapper",children:[he?g.jsxs("div",{style:{background:"var(--card-bg)",padding:"12px",borderRadius:"12px",border:"1px solid var(--border-subtle)"},children:[g.jsx("textarea",{className:"chat-textarea",value:qt,onChange:_e=>Mn(_e.target.value),rows:3,style:{width:"100%"}}),g.jsxs("div",{style:{display:"flex",gap:"8px",marginTop:"8px"},children:[g.jsx("button",{className:"btn-new-chat-pill",style:{width:"auto",padding:"6px 14px",fontSize:"0.8rem"},onClick:()=>G(K),children:"Save & Rerun"}),g.jsx("button",{className:"input-pill-btn",onClick:()=>vt(null),children:"Cancel"})]})]}):g.jsx("div",{className:"message-bubble",children:D.content}),!H&&!D.streaming&&g.jsxs("div",{className:"message-actions-bar",children:[g.jsxs("button",{className:"message-action-btn",onClick:()=>V(D.content,`msg-${K}`),children:[C===`msg-${K}`?g.jsx(m0,{size:12,color:"var(--accent-emerald)"}):g.jsx(v0,{size:12}),g.jsx("span",{children:C===`msg-${K}`?"Copied":"Copy"})]}),g.jsx("button",{className:"message-action-btn",onClick:()=>L(K,!0),style:{color:D.feedback===!0?"var(--accent-emerald)":"inherit"},children:g.jsx(T0,{size:12})}),g.jsx("button",{className:"message-action-btn",onClick:()=>L(K,!1),style:{color:D.feedback===!1?"var(--accent-rose)":"inherit"},children:g.jsx(k0,{size:12})})]})]})]},K)}),we&&g.jsxs("div",{className:"message-row assistant",children:[g.jsx("div",{className:"message-sender-avatar",children:g.jsx(ta,{size:26})}),g.jsx("div",{className:"message-content-wrapper",children:g.jsxs("div",{className:"message-bubble",style:{display:"flex",alignItems:"center",gap:10},children:[g.jsx("div",{className:"pulse-spinner"}),g.jsx("span",{style:{fontSize:"0.86rem",color:"var(--text-secondary)"},children:"Synthesizing answer from Knowledge Base..."})]})})]}),g.jsx("div",{ref:Fe})]}),g.jsx("div",{className:"pinned-bottom-composer",children:g.jsxs("div",{className:"chat-input-card",children:[w.length>0&&g.jsx("div",{className:"input-attachments-row",children:w.map(D=>g.jsxs("div",{className:"attachment-chip",children:[g.jsx(Rh,{size:12}),g.jsx("span",{children:D.file_name}),g.jsx("button",{className:"attachment-chip-remove",onClick:()=>Nt(D.id),children:g.jsx(Yo,{size:12})})]},D.id))}),g.jsxs("div",{className:"input-top-row",children:[g.jsx(ou,{size:18,className:"input-sparkle-icon"}),g.jsx("textarea",{className:"chat-textarea",placeholder:"Reply to Nexora AI...",value:pe,onChange:D=>de(D.target.value),onKeyDown:D=>{D.key==="Enter"&&!D.shiftKey&&(D.preventDefault(),Et())},rows:2})]}),g.jsxs("div",{className:"input-bottom-row",children:[g.jsxs("div",{className:"input-bottom-left",children:[g.jsx("button",{className:"input-attach-btn",title:"Attach document or screenshot",onClick:()=>{var D;return(D=Ot.current)==null?void 0:D.click()},"aria-label":"Attach file",children:g.jsx(Xo,{size:16})}),g.jsxs("button",{className:"input-pill-btn",onClick:()=>xe(!0),children:[g.jsx(Ko,{size:13}),g.jsx("span",{children:"Escalate"})]})]}),g.jsx("button",{className:"input-send-btn",disabled:!pe.trim()||we,onClick:()=>Et(),"aria-label":"Send message",children:g.jsx(Ah,{size:15})})]})]})})]}):g.jsx("div",{style:{flex:1,position:"relative",width:"100%",height:"calc(100vh - 65px)",overflow:"hidden"},children:g.jsx(Dx,{color:"#4fd1c5",secondaryColor:"#3b6cff",intensity:1.2,trailWidth:3,linger:1.4,glow:1.2,clickBurst:!0,theme:"dark",quality:window.innerWidth<900?"medium":"high",style:{width:"100%",height:"100%"},children:g.jsxs("div",{className:"welcome-container",children:[g.jsx("div",{className:"welcome-orb-wrapper",children:g.jsx(ta,{size:64})}),g.jsx("div",{className:"welcome-label",children:Te?`WELCOME BACK, ${Te}`:"WELCOME BACK"}),g.jsx("h1",{className:"welcome-heading",children:"Bring your ideas to life today"}),g.jsxs("div",{className:"chat-input-card",children:[w.length>0&&g.jsx("div",{className:"input-attachments-row",children:w.map(D=>g.jsxs("div",{className:"attachment-chip",children:[g.jsx(Rh,{size:12}),g.jsx("span",{children:D.file_name}),g.jsx("button",{className:"attachment-chip-remove",onClick:()=>Nt(D.id),children:g.jsx(Yo,{size:12})})]},D.id))}),g.jsxs("div",{className:"input-top-row",children:[g.jsx(ou,{size:18,className:"input-sparkle-icon"}),g.jsx("textarea",{className:"chat-textarea",placeholder:"Ask me anything...",value:pe,onChange:D=>de(D.target.value),onKeyDown:D=>{D.key==="Enter"&&!D.shiftKey&&(D.preventDefault(),Et())},rows:2})]}),g.jsxs("div",{className:"input-bottom-row",children:[g.jsxs("div",{className:"input-bottom-left",children:[g.jsx("input",{type:"file",ref:Ot,style:{display:"none"},multiple:!0,accept:".pdf,.png,.jpg,.jpeg,.webp,.docx,.txt,.csv",onChange:Ft}),g.jsx("button",{className:"input-attach-btn",title:"Attach documents or receipts",onClick:()=>{var D;return(D=Ot.current)==null?void 0:D.click()},"aria-label":"Attach file",children:g.jsx(Xo,{size:16})}),g.jsxs("div",{style:{position:"relative"},children:[g.jsxs("button",{className:"input-pill-btn",onClick:()=>A(!b),children:[g.jsx(Dh,{size:13}),g.jsx("span",{children:"Tools"}),g.jsx(Ih,{size:11})]}),b&&g.jsxs("div",{className:"tools-popover",children:[g.jsx("div",{className:"tools-popover-title",children:"Inference & Role Tuning"}),g.jsxs("div",{children:[g.jsxs("div",{style:{display:"flex",justifyContent:"space-between",fontSize:"0.75rem",color:"var(--text-secondary)",marginBottom:4},children:[g.jsx("span",{children:"Temperature"}),g.jsx("span",{children:Ve.toFixed(2)})]}),g.jsx("input",{type:"range",min:"0.0",max:"1.0",step:"0.05",value:Ve,onChange:D=>Pe(parseFloat(D.target.value)),style:{width:"100%"}})]}),g.jsxs("div",{children:[g.jsx("div",{style:{fontSize:"0.75rem",color:"var(--text-secondary)",marginBottom:4},children:"Role Access"}),g.jsxs("select",{value:Ce,onChange:D=>E(D.target.value),style:{width:"100%",background:"var(--page-bg)",border:"1px solid var(--border-subtle)",borderRadius:6,color:"white",padding:"4px 6px",fontSize:"0.78rem"},children:[g.jsx("option",{value:"customer",children:"Customer"}),g.jsx("option",{value:"support_agent",children:"Support Agent"}),g.jsx("option",{value:"admin",children:"Admin"})]})]})]})]})]}),g.jsx("button",{className:"input-send-btn",disabled:!pe.trim()||we,onClick:()=>Et(),"aria-label":"Send message",children:g.jsx(Ah,{size:15})})]})]}),g.jsxs("div",{className:"suggestions-row",children:[g.jsxs("div",{className:"suggestion-item-card",onClick:()=>Et("Do you provide paid internship opportunities with your courses?"),children:[g.jsxs("div",{className:"suggestion-card-top",children:[g.jsx("div",{className:"suggestion-icon-box",children:g.jsx(ou,{size:16,color:"var(--accent-teal)"})}),g.jsx(su,{size:16,className:"suggestion-arrow"})]}),g.jsxs("div",{children:[g.jsx("div",{className:"suggestion-title",children:"Internship Guidance"}),g.jsx("div",{className:"suggestion-desc",children:"Explore guaranteed internships, placements, and eligibility."})]})]}),g.jsxs("div",{className:"suggestion-item-card",onClick:()=>Et("What are the zero-cost EMI plans and refund policies?"),children:[g.jsxs("div",{className:"suggestion-card-top",children:[g.jsx("div",{className:"suggestion-icon-box",children:g.jsx(Ch,{size:16,color:"var(--accent-blue)"})}),g.jsx(su,{size:16,className:"suggestion-arrow"})]}),g.jsxs("div",{children:[g.jsx("div",{className:"suggestion-title",children:"Payment & EMI Plans"}),g.jsx("div",{className:"suggestion-desc",children:"Check flexible installment options and satisfaction policies."})]})]}),g.jsxs("div",{className:"suggestion-item-card",onClick:()=>Et("Can I run Power BI on macOS, or what are the alternatives?"),children:[g.jsxs("div",{className:"suggestion-card-top",children:[g.jsx("div",{className:"suggestion-icon-box",children:g.jsx(Ko,{size:16,color:"var(--accent-emerald)"})}),g.jsx(su,{size:16,className:"suggestion-arrow"})]}),g.jsxs("div",{children:[g.jsx("div",{className:"suggestion-title",children:"Software & Tech Specs"}),g.jsx("div",{className:"suggestion-desc",children:"Hardware compatibility, tool setup, and cloud environments."})]})]})]})]})})})}),c==="dashboard"&&He&&g.jsxs("div",{style:{flex:1,overflowY:"auto",padding:"2rem 2.5rem"},children:[g.jsx("h2",{style:{fontSize:"1.4rem",fontWeight:700,marginBottom:"1.25rem"},children:"Operational Telemetry & RAG Metrics"}),g.jsxs("div",{className:"dashboard-grid",children:[g.jsxs("div",{className:"kpi-card",children:[g.jsx("span",{className:"kpi-title",children:"Conversations"}),g.jsx("span",{className:"kpi-value",children:He.conversations_count})]}),g.jsxs("div",{className:"kpi-card",children:[g.jsx("span",{className:"kpi-title",children:"Questions Answered"}),g.jsx("span",{className:"kpi-value",children:He.questions_count})]}),g.jsxs("div",{className:"kpi-card",children:[g.jsx("span",{className:"kpi-title",children:"Tickets Generated"}),g.jsx("span",{className:"kpi-value",children:He.tickets_count})]}),g.jsxs("div",{className:"kpi-card",children:[g.jsx("span",{className:"kpi-title",children:"User Satisfaction"}),g.jsx("span",{className:"kpi-value",style:{color:"var(--accent-emerald)"},children:He.positive_feedback_pct!==void 0?`${He.positive_feedback_pct}%`:"98%"})]})]})]}),c==="tickets"&&g.jsxs("div",{style:{flex:1,overflowY:"auto",padding:"2rem 2.5rem"},children:[g.jsxs("div",{style:{display:"flex",justifyContent:"space-between",alignItems:"center",marginBottom:"1.25rem"},children:[g.jsx("h2",{style:{fontSize:"1.4rem",fontWeight:700},children:"Routed Support Tickets"}),g.jsxs("button",{className:"btn-new-chat-pill",style:{width:"auto",padding:"8px 16px"},onClick:()=>xe(!0),children:[g.jsx(Xo,{size:15})," Create Ticket"]})]}),g.jsxs("div",{style:{background:"var(--card-bg)",borderRadius:"var(--radius-lg)",border:"1px solid var(--border-subtle)",overflow:"hidden"},children:[Qe.map(D=>g.jsxs("div",{className:"ticket-row",children:[g.jsxs("div",{children:[g.jsx("div",{style:{fontWeight:600,color:"var(--text-primary)",marginBottom:2},children:D.issue_summary||"General Inquiry"}),g.jsxs("div",{style:{fontSize:"0.76rem",color:"var(--text-muted)"},children:["Contact: ",D.contact," • Assigned: ",D.assigned_team||"Tier 1"]})]}),g.jsx("span",{className:`priority-badge priority-${(D.priority||"medium").toLowerCase()}`,children:D.priority||"medium"})]},D.id||D.ticket_id)),Qe.length===0&&g.jsx("div",{style:{padding:"2rem",textAlign:"center",color:"var(--text-muted)",fontSize:"0.9rem"},children:"No active support cases recorded."})]})]})]}),Se&&g.jsx("div",{className:"modal-overlay",onClick:()=>fe(!1),children:g.jsxs("div",{className:"modal-card",onClick:D=>D.stopPropagation(),children:[g.jsxs("div",{style:{display:"flex",justifyContent:"space-between",alignItems:"center",marginBottom:"1.25rem"},children:[g.jsx("h3",{style:{fontSize:"1.15rem",fontWeight:700},children:"Security & Model Settings"}),g.jsx("button",{className:"sidebar-icon-btn",onClick:()=>fe(!1),children:g.jsx(Yo,{size:16})})]}),g.jsxs("div",{style:{display:"flex",flexDirection:"column",gap:"1rem"},children:[g.jsxs("div",{children:[g.jsxs("label",{style:{fontSize:"0.84rem",fontWeight:600,color:"var(--text-secondary)"},children:["Model Temperature: ",Ve.toFixed(2)]}),g.jsx("input",{type:"range",min:"0.0",max:"1.0",step:"0.05",value:Ve,onChange:D=>Pe(parseFloat(D.target.value)),style:{width:"100%",marginTop:"6px"}})]}),g.jsxs("div",{children:[g.jsx("label",{style:{fontSize:"0.84rem",fontWeight:600,color:"var(--text-secondary)"},children:"User Role (RAG Access Control)"}),g.jsxs("select",{value:Ce,onChange:D=>E(D.target.value),style:{width:"100%",padding:"8px 10px",background:"var(--page-bg)",border:"1px solid var(--border-subtle)",borderRadius:8,color:"white",marginTop:"6px"},children:[g.jsx("option",{value:"customer",children:"Customer (Public knowledge)"}),g.jsx("option",{value:"support_agent",children:"Support Agent (Internal guides)"}),g.jsx("option",{value:"admin",children:"Admin (Full access)"})]})]}),g.jsxs("div",{children:[g.jsx("label",{style:{fontSize:"0.84rem",fontWeight:600,color:"var(--text-secondary)"},children:"Regional Jurisdiction"}),g.jsxs("select",{value:ee,onChange:D=>Y(D.target.value),style:{width:"100%",padding:"8px 10px",background:"var(--page-bg)",border:"1px solid var(--border-subtle)",borderRadius:8,color:"white",marginTop:"6px"},children:[g.jsx("option",{value:"GLOBAL",children:"GLOBAL"}),g.jsx("option",{value:"US",children:"US (United States)"}),g.jsx("option",{value:"EU",children:"EU (GDPR Compliance)"}),g.jsx("option",{value:"IN",children:"IN (India)"})]})]}),g.jsx("button",{className:"btn-new-chat-pill",style:{justifyContent:"center",marginTop:"0.5rem"},onClick:()=>fe(!1),children:"Save Settings"})]})]})}),ke&&g.jsx("div",{className:"modal-overlay",onClick:()=>xe(!1),children:g.jsxs("div",{className:"modal-card",onClick:D=>D.stopPropagation(),children:[g.jsxs("div",{style:{display:"flex",justifyContent:"space-between",alignItems:"center",marginBottom:"1.25rem"},children:[g.jsx("h3",{style:{fontSize:"1.15rem",fontWeight:700},children:"Submit Support Case"}),g.jsx("button",{className:"sidebar-icon-btn",onClick:()=>xe(!1),children:g.jsx(Yo,{size:16})})]}),g.jsxs("div",{style:{display:"flex",flexDirection:"column",gap:"1rem"},children:[g.jsxs("div",{children:[g.jsx("label",{style:{fontSize:"0.84rem",fontWeight:600,color:"var(--text-secondary)"},children:"Customer Contact (Email / Phone)"}),g.jsx("input",{type:"text",placeholder:"e.g. user@example.com or +1-555-0199",className:"sidebar-search-input",style:{marginTop:"6px"},value:Me,onChange:D=>te(D.target.value)})]}),g.jsxs("div",{children:[g.jsx("label",{style:{fontSize:"0.84rem",fontWeight:600,color:"var(--text-secondary)"},children:"Issue Summary"}),g.jsx("textarea",{className:"chat-textarea",style:{background:"var(--page-bg)",border:"1px solid var(--border-subtle)",borderRadius:8,padding:"8px",marginTop:"6px",width:"100%"},placeholder:"Describe your issue...",rows:3,value:Le,onChange:D=>Ue(D.target.value)})]}),g.jsx("button",{className:"btn-new-chat-pill",style:{justifyContent:"center"},disabled:!Me.trim(),onClick:j,children:"Submit Ticket"})]})]})})]})}i0.createRoot(document.getElementById("root")).render(g.jsx(Qg.StrictMode,{children:g.jsx(Iw,{children:g.jsx(bx,{})})}));
