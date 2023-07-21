function uj_feladatstatisztikák_svgbe(svg, szelesseg, leptek, feladatok_json) {
    let feladatok = Object.keys(feladatok_json);
    let N = feladatok.length;
    let v = new Vaszon({svg: boxplot_svg, tengely:{x:{min:-5, max:13}, y:{min:-(N*2+1), max:3}}, leptek:{x:20, y:20}});
    // v.alapracs(); // debug!

    // SZÁZALÉKRÁCS
    for (let j = 0; j <= 10; j+=1) {
        v.vonal(new Pont({x:j, y:0}), new Pont({x:j, y:-(2*N)}), {
            styles:['stroke:white', 'stroke-opacity:0.5'],
        });
        v.szoveg(v.balfelsosarokpont(), `${j*10}%`, {
            styles: [`font-size:8pt`, `fill:white`], 
            transforms: [`translate${v.vaszon2svg(new Pont({x:j, y:0.5})).repr()}`, 'rotate(-90)'],
            'alignment-baseline': 'middle',
        })
    }
    
    // FELADATNEVEK
    for (let i = 0; i < N; i++) {
        const feladatnev = feladatok[i];
        v.szoveg(new Pont({x:-0.5, y:-1-2*i}), feladatnev, {
            styles: ['fill:white', 'font-size:10pt'],
            'text-anchor': 'end',
            'alignment-baseline': 'middle',
        });
    }

    // let ba = new Pont({x:3, y:-2}); 
    // let bf = new Pont({x:3, y:-1}); 
    // let ja = new Pont({x:5, y:-2}); 
    // let jf = new Pont({x:5, y:-1}); 
    // v.teglalap(ba, jf);




    // v.teglalap(new Pont({x:0, y:0}), new Pont({x:10, y:-2}), {
    //     styles: ['fill-opacity: 0.1', 'stroke-opacity: 0.5','stroke:yellow', 'stroke-width:2'],
    // });

    let w = 10;

    for (let i = 0; i < N; i++) {
        const feladat = feladatok[i];
        let feladat_pontja = feladatok_json[feladat].pont;
        let feladat_maxpontja = feladatok_json[feladat].maxpont;
        v.uj_sodrofa({
                O: new Pont({x:0, y:-0.5-(2*i + 1)}),
                w: w,
                h: 1,
                alapvastagsag: 1.5,
                medianvastagsag: 3,
                kvartilis: feladatok_json[feladat].kvartilis.map((k) => k / feladat_maxpontja),
                outliers: feladatok_json[feladat].outliers.map((o) => o / feladat_maxpontja),
                extreme_outliers: feladatok_json[feladat].extreme_outliers.map((o) => o / feladat_maxpontja),
                kiemelt_pont: feladat_pontja / feladat_maxpontja,
                szin: "white",
              });
    }

  
    //   elemek.push(szoveg([1 + w, -(i + 0.8)],`${feladat_pontja}/${feladat_maxpontja}`,['font-size:6pt', 'text-align:left', 'fill:white']));
    //   i += leptek * 2;
  }
  
