class Vaszon {
    constructor(canvas, step) {
        this.canvas = canvas;
        this.context = canvas.getContext('2d');
        this.origo = new Pont(Math.floor(this.canvas.width/2), Math.floor(this.canvas.height/2));
        this.step = step;
    }
  
    resize(w, h, o, step){
        this.canvas.width = w;
        this.canvas.height = h;
        this.origo = o;
        this.step = step;
        this.context = this.canvas.getContext('2d');
    }

    korvonal(o, r){
        this.context.beginPath();
        this.context.arc(o.x, o.y, r, 0, 2 * Math.PI);
        this.context.stroke();
    }
  
    ideiglenesen(property, value, action){
        this.context.save();
        this.context[property] = value;
        action();
        this.context.restore();
    }
  
    kor(o, r, linewidth, drawstyle, fillstyle){
        this.korlemez(o, r, drawstyle);
        this.korlemez(o, r-linewidth, fillstyle);
    }

    korlemez(o, r, fillstyle){

        this.context.save();
        this.context['fillStyle'] = fillstyle;
        
        let p = this.elhelyez(o);
        this.context.beginPath();
        this.context.arc(p.x, p.y, r, 0, 2 * Math.PI);
        this.context.fill();
        
        this.context.restore();
    }
  
    pontok_rajzolasa(pontlista){
        for (const p of this.pontok_elhelyezese(pontlista)) {
            this.kor(p, 3, 'black', 'black');
        }
    }
  
    pontok_elhelyezese(pontlista){
        let r = [];
        for (const p of pontlista) {
            r.push(this.elhelyez(p));
        }
        return r;
    }
  
    elhelyez(p){
        return p.tagonkent_szoroz(this.step.tagonkent_szoroz(new Pont(1,-1))).plusz(this.origo);
    }
    
    gorbe(pontlista, tension, isClosed, numOfSegments, showPoints) {
      let pontok = this.pontok_elhelyezese(pontlista);
        return this.drawCurve(Pont.koordinatalistaba_fejt(pontok), tension, isClosed, numOfSegments, showPoints);
    }
  
    drawCurve(ptsa, tension, isClosed, numOfSegments, showPoints) {
      this.context.beginPath();
      this.drawLines(Pont.getCurvePoints(ptsa, tension, isClosed, numOfSegments));
      this.context.stroke();
    }
  
    drawLines(pts) {
      this.context.moveTo(pts[0], pts[1]);
      for(let i=2;i<pts.length-1;i+=2){
        this.context.lineTo(pts[i], pts[i+1]);
      }
    }
  
    vonal(p, q, lw=1){
        let [a,b] = this.pontok_elhelyezese([p,q]);
        
        this.context.save();
        this.context.lineWidth = lw;
        
        this.context.beginPath();
        this.context.moveTo(a.x, a.y);
        this.context.lineTo(b.x, b.y);
        this.context.stroke();
        
        this.context.restore();
    }
    
    nyersvonal(px, py, qx, qy){
      this.context.beginPath();
      this.context.moveTo(px, py);
      this.context.lineTo(qx, qy);
      this.context.stroke();
    }
  
  
  
    koordinatarendszer_berajzolasa(vonalvastagsag = 1, szin = 'rgba(0,0,0,0.3)'){
  
      // let maxx = Math.floor(this.canvas.width/this.step.x)
      // let minx = -maxx
      // let maxy = Math.floor(this.canvas.height/this.step.y)
      // let miny = -maxy

        this.context.save();
        
        this.context.strokeStyle = szin;
        this.context.lineWidth = vonalvastagsag;
        
        for (let xx = 0; xx < this.canvas.width; xx+=this.step.x) {
            this.nyersvonal(xx, 0, xx, this.canvas.height);
        }
        for (let yy = 0; yy < this.canvas.height; yy+=this.step.y) {
            this.nyersvonal(0, yy, this.canvas.width, yy);      
        }
        
        this.context.strokeStyle = `rgba(0,0,0,1)`;
        this.vonal(new Pont(0, -1), new Pont(0, 1));
        this.vonal(new Pont(-1, 0), new Pont(1, 0));
        
        this.context.restore();
    }

    teglalap(BA, JA, JF, BF, lw, drawcolor, fillcolor){
        this.context.save();
        this.context.lineWidth = lw;
        // this.context.strokeStyle = drawcolor;
        // this.context.fillRect(BF.x, BF.y, JF.x-BF.x, BA.x-BF.x);
        // this.context.fillStyle = fillcolor;
        // this.context.rect(BF.x, BF.y, JF.x-BF.x, BA.x-BF.x);
        
        this.gorbe([BA, JA, JF, BF, BA, JA], 0);
        
        this.context.restore();
    }

    boxplot(kwargs){
        // kwargs = {O, w, h, kvartilis, outliers, extreme_outliers}
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

        let O = kwargs['O'];
        let w = kwargs['w'];
        let h = kwargs['h'];
        let kvartilis = kwargs['kvartilis'];
        let outliers = kwargs['outliers'];
        let extreme_outliers = kwargs['extreme_outliers'];
        let lw = kwargs['linewidth'];
        let mlw = kwargs['medianwidth'];
        
        let x = kvartilis.map(k => O.x + k * w);
        let y = [O.y, O.y+h/2, O.y + h];

        let MIN_A = new Pont(x[0], y[0]);
        let MIN_K = new Pont(x[0], y[1]);
        let MIN_F = new Pont(x[0], y[2]);
        this.vonal(MIN_A, MIN_F, lw);
        
        let IQR_BA = new Pont(x[1], y[0]);
        let IQR_BK = new Pont(x[1], y[1]);
        let IQR_BF = new Pont(x[1], y[2]);
        let IQR_JA = new Pont(x[3], y[0]);
        let IQR_JK = new Pont(x[3], y[1]);
        let IQR_JF = new Pont(x[3], y[2]);
        this.vonal(MIN_K, IQR_BK, lw);
        this.teglalap(IQR_BA, IQR_JA, IQR_JF, IQR_BF, lw, 'black', 'blue');
        
        let MED_A = new Pont(x[2], y[0]);
        let MED_F = new Pont(x[2], y[2]);
        this.vonal(MED_A, MED_F, mlw)
        
        let MAX_A = new Pont(x[4], y[0]);
        let MAX_K = new Pont(x[4], y[1]);
        let MAX_F = new Pont(x[4], y[2]);
        this.vonal(IQR_JK, MAX_K, lw);
        this.vonal(MAX_A, MAX_F, lw);

        let r = 0.25*h*this.step.x;
        for (const o of outliers) {
            this.kor(new Pont(O.x+o*w, y[1]), r, 1, 'black', 'white');
        }

        for (const eo of extreme_outliers) {
            this.kor(new Pont(O.x+eo*w, y[1]), r, 1, 'black', 'black');
        }
        

        this.kor(new Pont(O.x+kwargs['kiemelt_pont']*w, y[1]), r, 1, 'black', 'lightgreen');
        

    }

    // szovegdoboz(kwargs){
    //     let P = this.elhelyez(kwargs['P']);
    //     this.context.save();
    //     // this.context.translate(P.x, P.y);
    //     this.context.rotate(kwargs['forgatas']);
    //     this.context.font = kwargs['font'];
    //     this.context.textAlign = kwargs['align'];
    //     this.context.fillText(kwargs['szoveg'], P.x, P.y);
        
    //     this.context.restore();
    // }

    szovegdoboz(kwargs){
        let P = this.elhelyez(kwargs['P']);
        this.context.save();
        this.context.translate(P.x, P.y);
        this.context.rotate(kwargs['forgatas']);
        this.context.font = kwargs['font'];
        // context.fillStyle = kwargs['szin']; // green
        this.context.textAlign = kwargs['align'];
        this.context.fillText( kwargs['szoveg'], 0, 0 );
        this.context.restore();
    }
}
  