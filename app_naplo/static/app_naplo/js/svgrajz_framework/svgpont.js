// import Matek from './svgmatek.js';

class Pont {
    constructor(o) {
        let kulcsok = Object.keys(o);
        if (kulcsok.includes('x') && kulcsok.includes('y')){
            this.x = o.x;
            this.y = o.y;
            // this.sz = Matek.atg2(this.y, this.x);
            // this.r = Math.sqrt(x*x+y*y);
        } else if (kulcsok.includes('r') && kulcsok.includes('sz')) {
            // this.sz = kwargs['sz'];
            // this.r = kwargs['r'];
            this.x = o.r * Matek.cos(o.sz);
            this.y = o.r * Matek.sin(o.sz);
        } else {
            console.log('Nincsenek x-y kulcsok és r-sz kulcsok sem a konstruktor inputjában!')
        }
    }

    polar(){
        return {
            sz: Matek.atg2(this.y, this.x), 
            r: Math.sqrt(x*x+y*y)
        };
    }

    plusz(p){
        return new Pont({
            x: this.x+p.x, 
            y: this.y+p.y
        });
    }

    minusz(p){
        return new Pont({
            x: this.x-p.x, 
            y: this.y-p.y
        });
    }
    
    szoroz(szam){
        return new Pont({
            x: this.x*szam, 
            y: this.y*szam
        });
    }

    oszt(szam){
        return new Pont({
            x: this.x/szam, 
            y: this.y/szam
        });
    }

    szoroz_hadamard(p){
        return new Pont({
            x: this.x*p.x, 
            y: this.y*p.y
        });
    }

    oszt_hadamard(p){
        return new Pont({
            x: this.x/p.x, 
            y: this.y/p.y
        });
    }

    skalarszorzat(p){
        return this.x*p.x + this.y+p.y;
    }

    forgat(szog){
        let p = this.polar();
        return new Pont({
            sz: p.sz+szog, 
            r: p.r 
        });
    }

    tukroz_x(){
        return new Pont({
            x:this.x,
            y:-this.y
        });
    }

    tukroz_y(){
        return new Pont({
            x:-this.x,
            y:this.y
        });
    }

    static origo(){
        return new Pont({
            x:0, 
            y:0
        });
    }

    repr(){
        return `(${this.x},${this.y})`;
    }

    toString(){
        return `(${this.x},${this.y})`;
    }
}


