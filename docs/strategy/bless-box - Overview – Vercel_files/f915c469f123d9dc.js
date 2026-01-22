;!function(){try { var e="undefined"!=typeof globalThis?globalThis:"undefined"!=typeof global?global:"undefined"!=typeof window?window:"undefined"!=typeof self?self:{},n=(new e.Error).stack;n&&((e._debugIds|| (e._debugIds={}))[n]="be090a9c-4c50-24e9-390f-0d8d532e1914")}catch(e){}}();
(globalThis.TURBOPACK||(globalThis.TURBOPACK=[])).push(["object"==typeof document?document.currentScript:void 0,3748432,e=>{"use strict";e.i(2598434);var t=e.i(847684),n=e.i(7185353),r=e.i(8238875),i=e.i(8612999),a=e.i(5773208);let s={hard:{skeleton:"primary-light",content:"primary-dark"},soft:{skeleton:"secondary-light",content:"secondary-dark"}};function o(e,t){let n=e?"hard":"soft";return{track:"Navigation Phases ▲",color:s[n][t.phase],properties:[["Navigation Type",n]].concat(Object.entries(t).map(e=>{let[t,n]=e;return[t.split("_").map(e=>e.charAt(0).toUpperCase()+e.slice(1)).join(" "),String(n)]}))}}function l(e){let{children:r,...i}=e;return(0,t.jsxs)(t.Fragment,{children:[r,(0,t.jsx)(n.Suspense,{fallback:(0,t.jsx)("div",{hidden:!0,"data-navigation-marker":`${i.phase}-${i.label}`}),children:(0,t.jsx)(u,{...i})})]})}function u(e){let s,l,{phase:u,label:d,routeOverride:h}=e,g=(s=(0,r.usePathname)(),l=(0,r.useParams)(),(0,n.useMemo)(()=>{if(!l)return(0,i.computeRoute)(s,{});let{catchAll:e,...t}=l;return(0,i.computeRoute)(s,t)},[s,l])),f=h??g??"unknown",m=(0,n.useRef)(!1);(0,n.useEffect)(()=>{if(!m.current&&(m.current=!0,!c(u,"interactive",d)))return requestAnimationFrame(()=>{requestAnimationFrame(()=>{var e=u,t=f,n=d;let r=performance.now(),i={phase:e,route:t,target_env:"production",label:n,state:"interactive"};try{performance.measure(`${e} interactive`,{start:a.routerState.lastRouterTransition.startMsSinceOrigin,end:r,detail:{vercelNavigation:{isHardNavigation:a.routerState.isHardNavigation,attrs:i},devtools:o(a.routerState.isHardNavigation,i)}})}catch{}})}),()=>{"skeleton"===u||c(u,"unmounted",d)||0===a.routerState.lastRouterTransition.startMsSinceOrigin||requestAnimationFrame(()=>{let e={phase:u,route:f,label:d,target_env:"production",state:"unmounted"};performance.measure(`${u} unmount`,{start:a.routerState.lastRouterTransition.startMsSinceOrigin,end:performance.now(),detail:{vercelNavigation:{isHardNavigation:!1,attrs:e},devtools:o(a.routerState.isHardNavigation,e)}})})}},[u,f,d]);let j={phase:u,label:d,route:f,target_env:"production",state:"visible"};return(0,t.jsx)(t.Fragment,{children:(0,t.jsx)("script",{dangerouslySetInnerHTML:{__html:`
        requestAnimationFrame(() => {
          globalThis.__VERCEL_NAVIGATION_METRICS_RECORDED_MEASURES = globalThis.__VERCEL_NAVIGATION_METRICS_RECORDED_MEASURES || new Map();
          if (globalThis.__VERCEL_NAVIGATION_METRICS_RECORDED_MEASURES.has("${u} visible")) {
            
            return;
          }
          globalThis.__VERCEL_NAVIGATION_METRICS_RECORDED_MEASURES.set("${u} visible", "${d}");

          try {
            performance.measure("${u} visible", {
              end: performance.now(),
              detail: {
                vercelNavigation: {
                  isHardNavigation: true,
                  attrs: JSON.parse(${JSON.stringify(JSON.stringify(j))}),
                },
                devtools: JSON.parse(${JSON.stringify(JSON.stringify(o(!0,j)))})
              }
            });
          } catch {}
        });
      `}})})}function c(e,t,n){let r=(0,a.getRecordedMeasures)();return!!r.has(`${e} ${t}`)||(r.set(`${e} ${t}`,n||"unknown"),!1)}e.s(["ConditionalNavigationMarker",0,function(e){let{children:n,enabled:r,phase:i,label:a,routeOverride:s}=e;return(0,t.jsxs)(t.Fragment,{children:[n,r&&(0,t.jsx)(l,{phase:i,label:a,routeOverride:s})]})},"NavigationMarker",0,l],3748432)},835469,e=>{e.v({settingsGeneral:"team-settings-general-skeleton-module__uzFQ5G__settingsGeneral"})},5216091,e=>{"use strict";var t=e.i(847684),n=e.i(5255926),r=e.i(5807088),i=e.i(835469),a=e.i(3748432);function s(){return(0,t.jsx)(r.default,{height:80})}function o(){return(0,t.jsx)(r.default,{height:102})}function l(){return(0,t.jsx)(r.default,{height:55})}function u(){return(0,t.jsx)(r.default,{height:102})}function c(){return(0,t.jsx)(r.default,{height:81})}function d(){return(0,t.jsx)(n.Skeleton,{height:30,width:140})}function h(){return(0,t.jsx)(r.default,{height:81})}function g(){return(0,t.jsx)(r.default,{height:36})}function f(){return(0,t.jsx)(r.default,{height:56})}e.s(["TeamSettingsGeneralSkeleton",0,function(){return(0,t.jsxs)("main",{className:i.default.settingsGeneral,children:[(0,t.jsx)(a.NavigationMarker,{phase:"skeleton",label:"TeamSettingsGeneralSkeleton"}),(0,t.jsx)("section",{children:(0,t.jsx)(s,{})}),(0,t.jsx)("section",{children:(0,t.jsx)(o,{})}),(0,t.jsx)("section",{children:(0,t.jsx)(l,{})}),(0,t.jsx)("section",{children:(0,t.jsx)(u,{})}),(0,t.jsx)("section",{children:(0,t.jsx)(c,{})}),(0,t.jsx)("section",{children:(0,t.jsx)(d,{})}),(0,t.jsx)("section",{children:(0,t.jsx)(h,{})}),(0,t.jsx)("section",{children:(0,t.jsx)(g,{})}),(0,t.jsx)("section",{children:(0,t.jsx)(f,{})})]})}])}]);

//# debugId=be090a9c-4c50-24e9-390f-0d8d532e1914
//# sourceMappingURL=d17a216438cf8285.js.map