(function(){"use strict";var e={2631:function(e,n,t){var o=t(5130),s=t(6768);const r={key:0,class:"menu"},u=(0,s.Lk)("div",{id:"function"},[(0,s.Lk)("p",{class:"bg-red"},[(0,s.Lk)("strong",null,"기능들")]),(0,s.Lk)("ul",null,[(0,s.Lk)("li",null,"챗봇"),(0,s.Lk)("li",null,"병해충진단")])],-1),i=(0,s.Lk)("div",{id:"search_list"},[(0,s.Lk)("p",{class:"bg-red"},[(0,s.Lk)("strong",null,"검색 기록")])],-1),a={key:1,class:"no-menu"},l={class:"main"},c=(0,s.Lk)("div",null,[(0,s.Lk)("button",{id:"settings"})],-1),d={id:"chat"},f={class:"search"};function h(e,n,t,o,h,p){const g=(0,s.g2)("AppChatbot");return(0,s.uX)(),(0,s.CE)(s.FK,null,[h.show?((0,s.uX)(),(0,s.CE)("aside",r,[(0,s.Lk)("div",null,[(0,s.Lk)("button",{id:"hidden",onClick:n[0]||(n[0]=(...e)=>p.toggleShow&&p.toggleShow(...e))})]),u,i])):h.show?(0,s.Q3)("",!0):((0,s.uX)(),(0,s.CE)("aside",a,[(0,s.Lk)("button",{id:"show",onClick:n[1]||(n[1]=(...e)=>p.toggleShow&&p.toggleShow(...e))})])),(0,s.Lk)("main",l,[c,(0,s.Lk)("div",d,[(0,s.Lk)("div",f,[(0,s.bF)(g)])])])],64)}var p=t(4232);const g={class:"chat-bot"},v={class:"messages"},k=(0,s.Lk)("button",{type:"submit"},null,-1);function b(e,n,t,r,u,i){return(0,s.uX)(),(0,s.CE)("div",g,[(0,s.Lk)("div",v,[((0,s.uX)(!0),(0,s.CE)(s.FK,null,(0,s.pI)(u.messages,(e=>((0,s.uX)(),(0,s.CE)("div",{key:e.id,class:"message"},[(0,s.Lk)("div",{class:(0,p.C4)(`message-${e.sender}`)},(0,p.v_)(e.text),3)])))),128))]),(0,s.bo)((0,s.Lk)("input",{"onUpdate:modelValue":n[0]||(n[0]=e=>u.userInput=e),onKeyup:n[1]||(n[1]=(0,o.jR)(((...e)=>i.sendMessage&&i.sendMessage(...e)),["enter"])),placeholder:"메시지 입력..."},null,544),[[o.Jo,u.userInput]]),k])}t(4114);var m=t(4373),w={data(){return{userInput:"",messages:[]}},methods:{async sendMessage(){const e=this.userInput.trim();if(!e)return;this.addMessage("user",e);const n=await this.getAIResponse(e);this.addMessage("ai",n),this.userInput=""},addMessage(e,n){this.messages.push({id:Date.now(),sender:e,text:n})},async getAIResponse(e){try{const n=await m.A.post("AI_API_ENDPOINT",{prompt:e},{headers:{Authorization:"Bearer YOUR_API_KEY"}});return n.data.choices[0].text.trim()}catch(n){return console.error("AI 응답 오류:",n),"죄송합니다, 오류가 발생했습니다."}}}},y=t(1241);const L=(0,y.A)(w,[["render",b]]);var O=L,A={name:"App",data(){return{show:!0}},methods:{toggleShow(){this.show=!this.show}},components:{AppChatbot:O}};const C=(0,y.A)(A,[["render",h]]);var I=C;(0,o.Ef)(I).mount("#app")}},n={};function t(o){var s=n[o];if(void 0!==s)return s.exports;var r=n[o]={exports:{}};return e[o].call(r.exports,r,r.exports,t),r.exports}t.m=e,function(){var e=[];t.O=function(n,o,s,r){if(!o){var u=1/0;for(c=0;c<e.length;c++){o=e[c][0],s=e[c][1],r=e[c][2];for(var i=!0,a=0;a<o.length;a++)(!1&r||u>=r)&&Object.keys(t.O).every((function(e){return t.O[e](o[a])}))?o.splice(a--,1):(i=!1,r<u&&(u=r));if(i){e.splice(c--,1);var l=s();void 0!==l&&(n=l)}}return n}r=r||0;for(var c=e.length;c>0&&e[c-1][2]>r;c--)e[c]=e[c-1];e[c]=[o,s,r]}}(),function(){t.n=function(e){var n=e&&e.__esModule?function(){return e["default"]}:function(){return e};return t.d(n,{a:n}),n}}(),function(){t.d=function(e,n){for(var o in n)t.o(n,o)&&!t.o(e,o)&&Object.defineProperty(e,o,{enumerable:!0,get:n[o]})}}(),function(){t.g=function(){if("object"===typeof globalThis)return globalThis;try{return this||new Function("return this")()}catch(e){if("object"===typeof window)return window}}()}(),function(){t.o=function(e,n){return Object.prototype.hasOwnProperty.call(e,n)}}(),function(){t.r=function(e){"undefined"!==typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})}}(),function(){var e={524:0};t.O.j=function(n){return 0===e[n]};var n=function(n,o){var s,r,u=o[0],i=o[1],a=o[2],l=0;if(u.some((function(n){return 0!==e[n]}))){for(s in i)t.o(i,s)&&(t.m[s]=i[s]);if(a)var c=a(t)}for(n&&n(o);l<u.length;l++)r=u[l],t.o(e,r)&&e[r]&&e[r][0](),e[r]=0;return t.O(c)},o=self["webpackChunkhomepage"]=self["webpackChunkhomepage"]||[];o.forEach(n.bind(null,0)),o.push=n.bind(null,o.push.bind(o))}();var o=t.O(void 0,[504],(function(){return t(2631)}));o=t.O(o)})();
//# sourceMappingURL=app.e5bc9fa5.js.map