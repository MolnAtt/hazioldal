class Pont {
    constructor(x,y) {
        this.x = x;
        this.y = y;
    }
  
    static szamlista2parlista(szamlista){
      let r = [];
      for (let i = 0; i < array.length; i++) {
        r.push([i, szamlista[i]]);
      }
      return r;
    }
    
    static parlista2pontlista(parlista){
      return parlista.map(p => new Pont(p[0],p[1]));
    }
  
    static koordinatalistaba_fejt(pontlista){
      let klista = [];
      for (const pont of pontlista) {
        klista.push(pont.x);
        klista.push(pont.y);
      }
      return klista;
    }

    static illeszkedo_egyenes_meredeksege(P,Q){
      return (P.y-Q.y)/(P.x-Q.x)
    }

    static illeszkedo_egyenesek_metszespontja(A,B,C,D){
        if (A.x == B.x && C.x == D.x) 
            return undefined;
        if (A.x == B.x) 
            return new Pont(A.x, Pont.illeszkedo_egyenes_meredeksege(C,D)*(A.x-C.x)+C.y);
        if (C.x == D.x) 
            return new Pont(C.x, Pont.illeszkedo_egyenes_meredeksege(A,B)*(C.x-A.x)+A.y);

        let alfa = Pont.illeszkedo_egyenes_meredeksege(A,B);
        let gamma = Pont.illeszkedo_egyenes_meredeksege(C,D);
        let x = (alfa*A.x - gamma*C.x - A.y + C.y) / (alfa-gamma);
        let y = alfa(x - A.x) + A.y;
        return new Pont(x,y);  
    }

    copy(){
        return Pont(this.x, this.y);
    }
  
    plusz(that){
        return new Pont(this.x+that.x, this.y+that.y);
    }
  
    minusz(that){
        return new Pont(this.x-that.x, this.y-that.y);
    }
  
    tagonkent_szoroz(that){
        return new Pont(this.x*that.x, this.y*that.y);
    }
  
    skalaris_szorzat(that){
        return this.x*that.x + this.y*that.y;
    }
  
    
  
    // refaktorolni kéne ponthalmazokra...
    static getCurvePoints(pts, tension, isClosed, numOfSegments) {
  
      // use input value if provided, or use a default value	 
      tension = (typeof tension != 'undefined') ? tension : 0.5;
      isClosed = isClosed ? isClosed : false;
      numOfSegments = numOfSegments ? numOfSegments : 16;
    
      var _pts = [], res = [],	// clone array
          x, y,			// our x,y coords
          t1x, t2x, t1y, t2y,	// tension vectors
          c1, c2, c3, c4,		// cardinal points
          st, t, i;		// steps based on num. of segments
    
      // clone array so we don't change the original
      //
      _pts = pts.slice(0);
    
      // The algorithm require a previous and next point to the actual point array.
      // Check if we will draw closed or open curve.
      // If closed, copy end points to beginning and first points to end
      // If open, duplicate first points to befinning, end points to end
      if (isClosed) {
        _pts.unshift(pts[pts.length - 1]);
        _pts.unshift(pts[pts.length - 2]);
        _pts.unshift(pts[pts.length - 1]);
        _pts.unshift(pts[pts.length - 2]);
        _pts.push(pts[0]);
        _pts.push(pts[1]);
      }
      else {
        _pts.unshift(pts[1]);	//copy 1. point and insert at beginning
        _pts.unshift(pts[0]);
        _pts.push(pts[pts.length - 2]);	//copy last point and append
        _pts.push(pts[pts.length - 1]);
      }
    
      // ok, lets start..
    
      // 1. loop goes through point array
      // 2. loop goes through each segment between the 2 pts + 1e point before and after
      for (i=2; i < (_pts.length - 4); i+=2) {
        for (t=0; t <= numOfSegments; t++) {
    
          // calc tension vectors
          t1x = (_pts[i+2] - _pts[i-2]) * tension;
          t2x = (_pts[i+4] - _pts[i]) * tension;
    
          t1y = (_pts[i+3] - _pts[i-1]) * tension;
          t2y = (_pts[i+5] - _pts[i+1]) * tension;
    
          // calc step
          st = t / numOfSegments;
    
          // calc cardinals
          c1 =   2 * Math.pow(st, 3) 	- 3 * Math.pow(st, 2) + 1; 
          c2 = -(2 * Math.pow(st, 3)) + 3 * Math.pow(st, 2); 
          c3 = 	   Math.pow(st, 3)	- 2 * Math.pow(st, 2) + st; 
          c4 = 	   Math.pow(st, 3)	- 	  Math.pow(st, 2);
    
          // calc x and y cords with common control vectors
          x = c1 * _pts[i]	+ c2 * _pts[i+2] + c3 * t1x + c4 * t2x;
          y = c1 * _pts[i+1]	+ c2 * _pts[i+3] + c3 * t1y + c4 * t2y;
    
          //store points in array
          res.push(x);
          res.push(y);
    
        }
      }
    
      return res;
    }

    static if_undefined(valtozo, ertek){
        return (typeof valtozo == 'undefined') ? ertek : valtozo;
    }

    static getgorbitesipontok(pts, tension, isClosed, numOfSegments) {
  
        // use input value if provided, or use a default value	 
        tension = if_undefined(tension, 0.5);
        isClosed = if_undefined(isClosed,false);
        numOfSegments = if_undefined(numOfSegments,16);
      
        let _pts = [];
        let res = [];
        x, y,			// our x,y coords
            t1x, t2x, t1y, t2y,	// tension vectors
            c1, c2, c3, c4,		// cardinal points
            st, t, i;		// steps based on num. of segments

        _pts = pts.slice(0);
      
        // The algorithm require a previous and next point to the actual point array.
        // Check if we will draw closed or open curve.
        // If closed, copy end points to beginning and first points to end
        // If open, duplicate first points to befinning, end points to end

        let eleje = pts[0].copy()
        let vege = pts[pts.length - 1].copy()

        if (isClosed) {
          _pts.unshift(vege);
          _pts.unshift(vege);
          _pts.push(eleje);
        } else {
          _pts.unshift(eleje);
          _pts.push(vege);
        }
      
        // 1. loop goes through point array
        // 2. loop goes through each segment between the 2 pts + 1e point before and after
        for (let i=1; i < _pts.length - 1; i++) {
          for (t=0; t <= numOfSegments; t++) {
      
            // calc tension vectors
            t1x = (_pts[i+1].x - _pts[i-1].x) * tension;
            t2x = (_pts[i+2].x - _pts[i].x) * tension;
            t1y = (_pts[i+1].y - _pts[i-1].y) * tension;
            t2y = (_pts[i+2].y - _pts[i].y) * tension;
      
            // calc step
            st = t / numOfSegments;
      
            // calc cardinals
            c1 =   2 * Math.pow(st, 3) 	- 3 * Math.pow(st, 2) + 1; 
            c2 = -(2 * Math.pow(st, 3)) + 3 * Math.pow(st, 2); 
            c3 = 	   Math.pow(st, 3)	- 2 * Math.pow(st, 2) + st; 
            c4 = 	   Math.pow(st, 3)	- 	  Math.pow(st, 2);
      
            // calc x and y cords with common control vectors
            x = c1 * _pts[i].x	+ c2 * _pts[i+1].x + c3 * t1x + c4 * t2x;
            y = c1 * _pts[i].y	+ c2 * _pts[i+1].y + c3 * t1y + c4 * t2y;
      
            //store points in array
            res.push(Pont(x,y));
          }
        }
      
        return res;
      }
    
  }