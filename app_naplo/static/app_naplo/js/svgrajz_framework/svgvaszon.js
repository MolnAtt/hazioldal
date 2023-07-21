// import Pont from './svgpont.js'

class Vaszon {
    /**
     * a következő kulcsok kötelezőek:
     * - svg: az svg HTMLelement
     * - tengely: egy object, 'x' és 'y' tulajdonságokkal, amelyek mindegyike egy object 'min' és 'max' float tulajdonságokkal
     * 
     * a következő két tulajdonság közül PONTOSAN AZ EGYIK kell:
     * - leptek: egy object, 'x' és 'y' float tulajdonsággal: a rácsot képző egységtéglalap méretei.
     * - meret: egy object, 'x' és 'y' float tulajdonsággal: a teljes svg-fájl szélessége és magassága.
     */
    constructor(o) {
        let kulcsok = Object.keys(o);
        if(!kulcsok.includes('svg'))
            throw new Error('nem érkezett \'svg\' kulcs a konstruktorba!');
        this.svg = o.svg;

        if(!kulcsok.includes('tengely'))
            throw new Error('nem érkezett \'tengely\' kulcs a konstruktorba!');
            
        let tengelykulcsok = Object.keys(o.tengely);
        if(!tengelykulcsok.includes('x'))
            throw new Error('nem érkezett \'x\' kulcs a tengelybe a konstruktorban!');
        if(!tengelykulcsok.includes('y'))
            throw new Error('nem érkezett \'y\' kulcs a tengelybe a konstruktorban!');

        let xtengelykulcsok = Object.keys(o.tengely.x);
        if(!xtengelykulcsok.includes('min'))
            throw new Error('nem érkezett \'min\' kulcs az xtengelybe a konstruktorban!');
        if(!xtengelykulcsok.includes('max'))
            throw new Error('nem érkezett \'max\' kulcs az xtengelybe a konstruktorban!');
            
        let ytengelykulcsok = Object.keys(o.tengely.y);
        if(!ytengelykulcsok.includes('min'))
            throw new Error('nem érkezett \'min\' kulcs az ytengelybe a konstruktorban!');
        if(!ytengelykulcsok.includes('max'))
            throw new Error('nem érkezett \'max\' kulcs az ytengelybe a konstruktorban!');
        
        this.tengely = o.tengely; 
        
        if(!kulcsok.includes('leptek') && !kulcsok.includes('meret'))
            throw new Error('\'leptek\' és \'meret\' kulcsok egyike sem szerepel a konstruktorban!');
        
        if(kulcsok.includes('leptek') && kulcsok.includes('meret'))
            throw new Error('\'leptek\' és \'meret\' kulcsok egyszerre szerepelnek a konstruktorban!');
        
        if(kulcsok.includes('leptek')){
            let leptekkulcsok = Object.keys(o.leptek);
            if(!leptekkulcsok.includes('x'))
                throw new Error('nem érkezett \'x\' kulcs a léptékbe a konstruktorban!');
            if(!leptekkulcsok.includes('y'))
                throw new Error('nem érkezett \'y\' kulcs a léptékbe a konstruktorban!');

            this.leptek = o.leptek;
            this.meretvaltoztatas(
                this.tengely.x.max*this.leptek.x - this.tengely.x.min*this.leptek.x, 
                this.tengely.y.max*this.leptek.y - this.tengely.y.min*this.leptek.y
                );
        } else {// if(kulcsok.includes('meret'))
            this.meretvaltoztatas(o.meret.x, o.meret.y);
            this.leptek = {
                x: o.meret.x/(this.tengely.x.max - this.tengely.x.min),
                y: o.meret.y/(this.tengely.y.max - this.tengely.y.min)
            };
        }

        this.origo = new Pont({
            x: this.tengely.x.min,
            y: this.tengely.y.max
        }).szoroz_hadamard(this.leptek).tukroz_y();
    }

    /**
     * Azt mondja meg, hogy ami az svg-n (x,y) koordinátájú pont, az a váaszon saját (szokásos) koordinátarendszerében milyen koordinátájú pont.
     * @param {Pont} p 
     * @returns Pont
     */
    svg2vaszon(p){
        return p.minusz(this.origo).tukroz_x().oszt_hadamard(this.leptek);
    }

    svg2vaszon_origonelkul(p){
        return p.tukroz_x().oszt_hadamard(this.leptek);
    }




    /**
     * Azt mondja meg, hogy ami a vásznon (x,y) koordinátájú pont, az az svg saját (fejjel lefele fordított) koordinátarendszerében milyen koordinátájú pont.
     * @param {Pont} p 
     * @returns Pont
     */
    vaszon2svg(p){
        return p.szoroz_hadamard(this.leptek).tukroz_x().plusz(this.origo);
    }
    vaszon2svg_origonelkul(p){
        return p.szoroz_hadamard(this.leptek);
    }

    tartalmazza(p){
        return this.xtengely.min<=p.x && this.ytengely.min<=p.y && p.x<=this.xtengely.max && p.y<=this.ytengely.max;
    }

    meretvaltoztatas(x, y){
        this.svg.setAttribute('width' , x);
        this.svg.setAttribute('height', y);
    }
    
    meret(){
        return {
            x:this.svg.getAttribute('width' , x),
            y:this.svg.getAttribute('height', y)
        }
    }

    balfelsosarokpont(){
        return new Pont({x:this.tengely.x.min, y:this.tengely.y.max});
    }

    vonal(p, q, o={styles:['stroke:red', 'stroke-width:1', 'stroke-opacity=0.1']}){
        let line = Vaszon.ujSVG('line');
        p = this.vaszon2svg(p);
        q = this.vaszon2svg(q);
        line.setAttribute('x1',p.x);
        line.setAttribute('y1',p.y);
        line.setAttribute('x2',q.x);
        line.setAttribute('y2',q.y);
        this.egyeb_attributumok(line, o);
        this.svg.appendChild(line);
    }
    
    
    teglalap(ba, jf, o={styles:['fill:red']}){
        let rectangle = Vaszon.ujSVG('rect');
        let at = jf.minusz(ba); // átlóvektor
        // console.log(`ba: ${ba}`);
        // console.log(`jf: ${jf}`);
        // console.log(`at: ${at}`);
        let svg_ba = new Pont({x:this.vaszon2svg(ba).x, y:this.vaszon2svg(jf).y});
        // console.log(`svg_ba: ${svg_ba}`);
        let svg_at = this.vaszon2svg_origonelkul(at);
        // console.log(`svg_at: ${svg_at}`);

        rectangle.setAttribute('x',svg_ba.x);
        rectangle.setAttribute('y',svg_ba.y);
        // console.log(`width:${svg_at.x}`);
        rectangle.setAttribute('width',svg_at.x);
        // console.log(`height:${svg_at.y}`);
        rectangle.setAttribute('height',svg_at.y);
        this.egyeb_attributumok(rectangle, o);
        this.svg.appendChild(rectangle);
    }

    kor(k, r, o={styles:['fill:red']}){
        let ellipse = Vaszon.ujSVG('ellipse');
        console.log(`k: ${k}`);
        k = this.vaszon2svg(k);
        console.log(`k átváltva: ${k}`);
        ellipse.setAttribute('cx',k.x);
        ellipse.setAttribute('cy',k.y);
        ellipse.setAttribute('rx',r*this.leptek.x);
        ellipse.setAttribute('ry',r*this.leptek.y);
        this.egyeb_attributumok(ellipse, o);
        this.svg.appendChild(ellipse);
    }
    
    szoveg(p, s, o={styles:['fill:red']}){
        let text = Vaszon.ujSVG('text');
        p = this.vaszon2svg(p);
        text.setAttribute('x',p.x);
        text.setAttribute('y',p.y);
        text.innerHTML = s;
        this.egyeb_attributumok(text, o);
        this.svg.appendChild(text);    
    }

    egyeb_attributumok(svgnode, o){
        let o_kulcsai = Object.keys(o);
        if(o_kulcsai.includes('styles') && 0<o.styles.length){
            svgnode.setAttribute('style', o.styles.join(';'));
        }

        if(o_kulcsai.includes('transforms') && 0<o.transforms.length){
            svgnode.setAttribute('transform', o.transforms.join(' '));
        }
        
        for (const o_kulcs of o_kulcsai) {
            if(o_kulcs!='styles'&& o_kulcs!='transforms'){
                svgnode.setAttribute(o_kulcs, o[o_kulcs]);                
            }
        }
    }

    alapracs(){
        for (let x = this.tengely.x.min; x <= this.tengely.x.max; x+=1) {            
            this.vonal(new Pont({x:x, y:this.tengely.y.min}), new Pont({x:x, y:this.tengely.y.max}));
        }
        for (let y = this.tengely.y.min; y <= this.tengely.y.max; y+=1) {            
            this.vonal(new Pont({y:y, x:this.tengely.x.min}), new Pont({y:y, x:this.tengely.x.max}));
        }
        this.kor(Pont.origo(), 0.2);
    }


    static ujSVG(elementname){return document.createElementNS('http://www.w3.org/2000/svg', elementname);}

    uj_sodrofa(o){
        // kwargs = {O, w, h, kvartilis, outliers, extreme_outliers, alapvastagsag, medianvastagsag, kiemelt_pont }
        // boxplot = {[0,0], 100, 100, kvartilis, outliers, extreme_outliers, alapvastagsag, medianvastagsag, kiemelt_pont }
        /*
            x[0]         x[1]    x[2]          x[3]        x[4]
                                MED_F
        MIN_F|      IQR_BF|-------|-------------|IQR_JF     | MAX_F     y[2]
             |            |       |             |           |
        MIN_K|------------|IQR_BK |       IQR_JK|-----------| MAX_K     y[1]
             |            |       |             |           |
        MIN_A|      IQR_BA|-------|-------------|IQR_JA     | MAX_A     y[0]
                                MED_A
        */
      
        // console.log('ez van most a kwargsban')
        // console.log(o);
      
        let O = o['O'];
        let w = o['w'];
        let h = o['h'];
        let kvartilis = o['kvartilis'];
        let outliers = o['outliers'];
        let extreme_outliers = o['extreme_outliers'];
        let lw = o['alapvastagsag'];
        let mlw = o['medianvastagsag'];
        let stroke_color = 'rgb(255,255,255)';

        
        let x = kvartilis.map(k => O.x + k * w);
        let y = [O.y, O.y+h/2, O.y + h];
        // console.log(y);
      
        let MIN_A = new Pont({x:x[0], y:y[0]});
        let MIN_K = new Pont({x:x[0], y:y[1]});
        let MIN_F = new Pont({x:x[0], y:y[2]});
        this.vonal(MIN_A, MIN_F, {styles:[`stroke:${stroke_color}`, `stroke-width:${lw}`]});
        
        let IQR_BA = new Pont({x:x[1], y:y[0]});
        let IQR_BK = new Pont({x:x[1], y:y[1]});
        let IQR_BF = new Pont({x:x[1], y:y[2]});
        let IQR_JA = new Pont({x:x[3], y:y[0]});
        let IQR_JK = new Pont({x:x[3], y:y[1]});
        let IQR_JF = new Pont({x:x[3], y:y[2]});
        this.vonal(MIN_K, IQR_BK, {styles:[`stroke:${stroke_color}`, `stroke-width:${lw}`]});
        
        // console.log(`bal alsó: ${IQR_BA}`);
        // console.log(`jobb felső: ${IQR_JF}`);
        this.teglalap(IQR_BA, IQR_JF, {styles:[`stroke:${stroke_color}`, `stroke-width:${lw}`]});
        
        let MED_A = new Pont({x:x[2], y:y[0]});
        let MED_F = new Pont({x:x[2], y:y[2]});
        this.vonal(MED_A, MED_F, {styles:[`stroke:${stroke_color}`, `stroke-width:${mlw}`]});
        
        let MAX_A = new Pont({x:x[4], y:y[0]});
        let MAX_K = new Pont({x:x[4], y:y[1]});
        let MAX_F = new Pont({x:x[4], y:y[2]});
        this.vonal(IQR_JK, MAX_K, {styles:[`stroke:${stroke_color}`, `stroke-width:${lw}`]});
        this.vonal(MAX_A, MAX_F, {styles:[`stroke:${stroke_color}`, `stroke-width:${lw}`]});
        
        let r = 0.2*h;
        for (const ol of outliers) {
            console.log(`ol:${ol}`);
            this.kor(new Pont({x:O.x+ol*w, y:y[1]}), r, {styles: [`stroke:${stroke_color}`, `fill:black`, `stroke-width:${lw}`]});
        }
      
        for (const eol of extreme_outliers) {
            this.kor(new Pont({x:O.x+eol*w, y:y[1]}), r, {styles:[`stroke:${stroke_color}`, `fill:white`, `stroke-width:${lw}`]});
        }
        
      
        if ( 0 <= o['kiemelt_pont']){
          this.kor(new Pont({x:O.x+o['kiemelt_pont']*w, y:y[1]}), r, {styles: [`stroke:rgb(255,255,255)`, `fill:#0097FB`, `stroke-width:${lw}`]});
        }      
      }
}
