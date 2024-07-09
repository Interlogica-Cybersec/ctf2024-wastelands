function particles() {
    let e, t, i;
    !function () {
        "undefined" == typeof opacity ? opacity = 100 : Number.isFinite(opacity) && 0 <= opacity && opacity <= 100 ? opacity : (opacity = 100, console.log("'opacity' must be a finite number between 0 and 100. Using default of '100'."));
        "undefined" == typeof numParticles ? numParticles = 10 : Number.isFinite(numParticles) ? numParticles : (numParticles = 10, console.log("'numParticles' must be a finite number. Using default of '5'."));
        "undefined" == typeof sizeMultiplier ? sizeMultiplier = 5 : Number.isFinite(sizeMultiplier) ? sizeMultiplier : (sizeMultiplier = 5, console.log("'sizeMultiplier' must be a finite number. Using default of '5'."));
        "undefined" == typeof width ? width = 1 : Number.isInteger(width) && width > 0 ? width : (width = 1, console.log("'width' must be an integer number of pixels greater than 0. Using default of '1'."));
        "undefined" == typeof connections ? connections = !0 : "boolean" == typeof connections ? connections : (connections = !0, console.log("'connections' must be either 'true' or 'false'. Using default of 'true'."));
        "undefined" == typeof connectionDensity ? connectionDensity = 1 / 15 * 100 : Number.isFinite(connectionDensity) && connectionDensity > 1 ? connectionDensity = 1 / connectionDensity * 100 : (connectionDensity = 1 / 15 * 100, console.log("'connectionDensity' must be a finite number greater than 1. Using default of '15'."));
        "undefined" == typeof noBounceH ? noBounceH = !1 : "boolean" == typeof noBounceH ? noBounceH : (noBounceH = !1, console.log("'noBounceH' must be either 'true' or 'false'. Using default of 'false'."));
        "undefined" == typeof noBounceV ? noBounceV = !1 : "boolean" == typeof noBounceV ? noBounceV : (noBounceV = !1, console.log("'noBounceV' must be either 'true' or 'false'. Using default of 'false'."));
        "undefined" == typeof speed ? speed = 50 : Number.isInteger(speed) && 0 <= speed && speed <= 1e3 ? speed : (speed = 50, console.log("'speed' must be an integer between 1-1000. Using default of '50'."));
        "undefined" == typeof speedH ? speedH = 1 : Number.isInteger(speedH) && -1e3 <= speedH && speedH <= 1e3 ? (speedH, speed = 1) : (speedH = 1, console.log("'speedH' must be an integer between -1000 and 1000. Using default of '1'."));
        "undefined" == typeof speedV ? speedV = 1 : Number.isInteger(speedV) && -1e3 <= speedV && speedV <= 1e3 ? (speedV, speed = 1) : (speedV = 1, console.log("'speedV' must be an integer between -1000 and 1000. Using default of '1'."));
        "undefined" == typeof avoidMouse ? avoidMouse = !0 : "boolean" == typeof avoidMouse ? avoidMouse : (avoidMouse = !0, console.log("'avoidMouse' must be either 'true' or 'false'. Using default of 'true'."));
        "undefined" == typeof hover ? hover = !0 : "boolean" == typeof hover ? hover : (hover = !0, console.log("'hover' must be either 'true' or 'false'. Using default of 'true'."))
    }(), function () {
        0 === getComputedStyle(document.documentElement).getPropertyValue("--col-particle").length ? (e = "#000000", console.log("CSS variable '--col-particle' is not set. Using 'black' (#000000).")) : e = getComputedStyle(document.documentElement).getPropertyValue("--col-particle");
        0 === getComputedStyle(document.documentElement).getPropertyValue("--col-particle-stroke").length ? (t = "#000000", console.log("CSS variable '--col-particle-stroke' is not set. Using 'black' (#000000).")) : t = getComputedStyle(document.documentElement).getPropertyValue("--col-particle-stroke");
        !0 === hover && 0 === getComputedStyle(document.documentElement).getPropertyValue("--col-particle-stroke-hover").length ? (i = "#ff0000", console.log("CSS variable '--col-particle-stroke-hover' is not set. Using 'red' (#ff0000).")) : i = getComputedStyle(document.documentElement).getPropertyValue("--col-particle-stroke-hover")
    }();
    const n = document.getElementById("particles"), o = n.getContext("2d");
    let s;
    n.width = window.innerWidth, n.height = window.innerHeight, speed = 0 !== speed ? speed / 100 : 0, opacity /= 100, n.style.opacity = opacity;
    let d = {x: void 0, y: void 0, radius: n.height / 80 * (n.width / 80)};
    window.addEventListener("mousemove", function (e) {
        d.x = e.x, d.y = e.y
    });

    class l {
        constructor(e, t, i, n, o) {
            this.x = e, this.y = t, this.directionX = i, this.directionY = n, this.size = o
        }

        draw() {
            o.beginPath(), o.arc(this.x, this.y, this.size, 0, 2 * Math.PI, !1), o.fillStyle = e, o.fill()
        }

        update() {
            if (!0 === noBounceH && speedH > 0 ? this.x > n.width && (this.x = 0) : !0 === noBounceH && speedH < 0 ? this.x < 0 && (this.x = n.width) : (this.x > n.width || this.x < 0) && (this.directionX = -this.directionX), !0 === noBounceV && speedV > 0 ? this.y > n.height && (this.y = 0) : !0 === noBounceV && speedV < 0 ? this.y < 0 && (this.y = n.height) : (this.y > n.height || this.y < 0) && (this.directionY = -this.directionY), avoidMouse) {
                let e = d.x - this.x, t = d.y - this.y;
                Math.sqrt(e * e + t * t) < d.radius + this.size && (d.x < this.x && this.x < n.width - 10 * this.size && (this.x += 10), d.x > this.x && this.x > 10 * this.size && (this.x -= 10), d.y < this.y && this.y < n.height - 10 * this.size && (this.y += 10), d.y > this.y && this.y > 10 * this.size && (this.y -= 10))
            }
            0 !== speed && (this.x += this.directionX * speed * speedH, this.y += this.directionY * speed * speedV), this.draw()
        }
    }

    function r() {
        s = [];
        let e = .01 * n.width;
        for (let t = 0; t < e * numParticles; t++) {
            let e = Math.random() * sizeMultiplier + 1, t = Math.random() * (innerWidth - 2 * e - 2 * e) + 2 * e;
            noBounceH ? directionX = 5 * Math.random() : directionX = 5 * Math.random() - 2.5;
            let i = Math.random() * (innerHeight - 2 * e - 2 * e) + 2 * e;
            noBounceV ? directionY = 5 * Math.random() : directionY = 5 * Math.random() - 2.5, s.push(new l(t, i, directionX, directionY, e))
        }
    }

    window.addEventListener("resize", function () {
        n.width = innerWidth, n.height = innerHeight, d.radius = n.height / 80 * (n.width / 80), r()
    }), window.addEventListener("mouseout", function () {
        d.x = void 0, d.y = void 0
    }), r(), function e() {
        requestAnimationFrame(e), o.clearRect(0, 0, innerWidth, innerHeight);
        for (let e = 0; e < s.length; e++) s[e].update();
        connections && function () {
            let e = 1;
            for (let l = 0; l < s.length; l++) for (let r = l; r < s.length; r++) {
                let c = (s[l].x - s[r].x) * (s[l].x - s[r].x) + (s[l].y - s[r].y) * (s[l].y - s[r].y);
                if (c < n.width / connectionDensity * (n.height / connectionDensity)) {
                    if (e = 1 - c / 2e4, hover) {
                        let n = d.x - s[l].x, r = d.y - s[l].y;
                        Math.sqrt(n * n + r * r) < 200 ? (o.globalAlpha = e, o.strokeStyle = i) : (o.globalAlpha = e, o.strokeStyle = t)
                    } else o.globalAlpha = e, o.strokeStyle = t;
                    o.lineWidth = width, o.beginPath(), o.moveTo(s[l].x, s[l].y), o.lineTo(s[r].x, s[r].y), o.stroke()
                }
            }
        }()
    }()
}