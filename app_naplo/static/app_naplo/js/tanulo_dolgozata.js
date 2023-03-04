function szazalekracs(v, N, leptek){
    for (let j = 0; j <= 10; j++) {
        v.szovegdoboz({
            'P': new Pont(j+.25,1.5),
            'szoveg': `${j*10}%`, 
            'font': '10px serif', 
            'align': 'center',
            'forgatas': -Math.PI/2,
        });
        
        let F = new Pont(j,0);
        let A = new Pont(j,-N*leptek);
        
        v.vonal(F, A, 0.3);
    }
}

function feladatstatisztikák(v, feladatok_json){
    let leptek = 1;
    let feladatok = Object.keys(feladatok_json);
    let N = feladatok.length

    v.resize(300, N*40, new Pont(100, 50), new Pont(10,10));
    szazalekracs(v, N, leptek*2);
    let i = 1;
    for (const feladat of feladatok) {
        
        v.szovegdoboz({
            'P': new Pont(-1, -(i+.8)),
            'szoveg': feladat, 
            'font': '10px serif', 
            'align': 'right',
            'forgatas': 0,
        });
    

        let feladat_pontja = feladatok_json[feladat].pont;
        let feladat_maxpontja = feladatok_json[feladat].maxpont;

        let w  = 10;
        

        v.boxplot({
            'O': new Pont(0,-(i+1)), 
            'w': w, 
            'h': leptek, 
            'linewidth': 1.5,
            'medianwidth': 4,
            'kvartilis': feladatok_json[feladat].kvartilis.map(k => k/feladat_maxpontja), 
            'outliers' : feladatok_json[feladat].outliers.map(o => o/feladat_maxpontja), 
            'extreme_outliers': feladatok_json[feladat].extreme_outliers.map(o => o/feladat_maxpontja), 
            'kiemelt_pont': feladat_pontja/feladat_maxpontja,
        });

        v.szovegdoboz({
            'P': new Pont(1+w, -(i+.8)),
            'szoveg': `${feladat_pontja}/${feladat_maxpontja}`, 
            'font': '10px serif', 
            'align': 'left',
            'forgatas': 0,
        });
    
    
        i+=leptek*2;
    }
    
    
}

function osztalygrafikon(v, ponthatar, IQR_grafikon){
    let w = 250;
    let h = 250;
    v.resize(w, h, new Pont(0.05*w, 0.95*h), new Pont(0.009*w,0.009*h));

    let BBA= new Pont(0, 0);
    let BBF = new Pont(0, 100);
    let BJF = new Pont(25, 100);
    let BJA = new Pont(25, 0);
    v.teglalap(BBA, BBF, BJF, BJA, 1, 'black', 'gray');
    
    let JBA= new Pont(75, 0);
    let JBF = new Pont(75, 100);
    let JJF = new Pont(100, 100);
    let JJA = new Pont(100, 0);
    
    v.teglalap(JBA, JBF, JJF, JJA, 1, 'black', 'gray');

    v.teglalap(BBA, BBF, JJF, JJA, 1, 'black', 'gray');

    let jegyek = Object.keys(ponthatar);
    for (const jegy of jegyek) {
        let magassag = ponthatar[jegy];
        v.szovegdoboz({
            'P': new Pont(12.5, magassag),
            'szoveg': jegy, 
            'font': '10px serif', 
            'align': 'center',
            'forgatas': 0,
        });   

        v.szovegdoboz({
            'P': new Pont(87.5, magassag),
            'szoveg': `${ponthatar[jegy]}%`, 
            'font': '10px serif', 
            'align': 'center',
            'forgatas': 0,
        });   

        if (1<jegy.length){
            // console.log(`${jegy}: ${jegy.length}`);
            v.vonal(new Pont(0, magassag), new Pont(100, magassag), .1);
        } else {
            v.vonal(new Pont(0, magassag), new Pont(100, magassag), .5);
        }

        let honnan = 25;
        let meddig = 75;
        let tav = meddig-honnan;
        let pontleptek = tav / (IQR_grafikon.length-1);

        pontlista = [];
        for (let i = 0; i < IQR_grafikon.length; i++) {
            let P = new Pont(honnan+i*pontleptek, 100*IQR_grafikon[i]);
            // v.kor(P, 2, 1, 'black', 'black');
            pontlista.push(P);
        }

        v.gorbe(pontlista, 0.2); //default tension=0.5
    }

}

async function main(){
    let csoport = document.querySelectorAll('.csoport')[0];
    console.log('innen kérdezem le az adatokat:')
    let url = `https://szlgbp.info/naplo/api/post/dolgozat/read/${csoport.value}/${dolgozatslug.value}/`;
    console.log(url);
    let adatok = await olvaso_fetch(url);
    console.log('ezek az adatok jöttek vissza:')
    console.log(adatok);
    
    let v = new Vaszon(canvaselem, new Pont(10, 10));
    // v.koordinatarendszer_berajzolasa(2, 'rgba(0,0,0,0.1)');
    
    // feladatstatisztikák(v,feladatok_json);
    feladatstatisztikák(v,adatok.feladatonkent);
    
    let w = new Vaszon(canvaselem2, new Pont(10, 10));
    // w.koordinatarendszer_berajzolasa(2, 'rgba(0,0,0,0.1)');
    // osztalygrafikon(w, ponthatar, IQR_grafikon);
    console.log('ezek a ponthatárok');
    console.log(adatok.ponthatar);
    console.log('ez az iqr-grafikon');
    console.log(adatok.statisztika.IQR_grafikon);

    osztalygrafikon(w,adatok.ponthatar, adatok.statisztika.IQR_grafikon);
}

// let feladatok_json = {
//     "Formulafa": {
//         "pont": 0.0,
//         "maxpont": 1.0,
//         "atlag": 1.0,
//         "modusz": [
//             1.0
//         ],
//         "kvartilis": [
//             1.0,
//             1.0,
//             1.0,
//             1.0,
//             1.0
//         ],
//         "boxplot-min": 1.0,
//         "boxplot-max": 1.0,
//         "outliers": [],
//         "extreme_outliers": []
//     },
//     "Kétváltozós": {
//         "pont": 1.0,
//         "maxpont": 1.0,
//         "atlag": 1.0,
//         "modusz": [
//             1.0
//         ],
//         "kvartilis": [
//             1.0,
//             1.0,
//             1.0,
//             1.0,
//             1.0
//         ],
//         "boxplot-min": 1.0,
//         "boxplot-max": 1.0,
//         "outliers": [],
//         "extreme_outliers": []
//     },
//     "Háromváltozós": {
//         "pont": 2.0,
//         "maxpont": 2.0,
//         "atlag": 1.89,
//         "modusz": [
//             2.0
//         ],
//         "kvartilis": [
//             1.0,
//             2.0,
//             2.0,
//             2.0,
//             2.0
//         ],
//         "boxplot-min": 2.0,
//         "boxplot-max": 2.0,
//         "outliers": [
//             1.0,
//             1.0
//         ],
//         "extreme_outliers": [
//             1.0,
//             1.0
//         ]
//     },
//     "Következtetés": {
//         "pont": 0.0,
//         "maxpont": 2.0,
//         "atlag": 1.56,
//         "modusz": [
//             2.0
//         ],
//         "kvartilis": [
//             1.0,
//             1.0,
//             2.0,
//             2.0,
//             2.0
//         ],
//         "boxplot-min": 1.0,
//         "boxplot-max": 2.0,
//         "outliers": [],
//         "extreme_outliers": []
//     }
// };

// let ponthatar = {
//     "1/2": 28.0,
//     "2": 33.0,
//     "2/3": 45.0,
//     "3": 50.0,
//     "3/4": 61.0,
//     "4": 66.0,
//     "4/5": 82.0,
//     "5": 87.0,
//     "5*": 100.0
// };

// let IQR_grafikon = [
//     0.6666666666666666,
//     0.6666666666666666,
//     0.6666666666666666,
//     0.6666666666666666,
//     0.6666666666666666,
//     0.6666666666666666,
//     0.6666666666666666,
//     0.8333333333333334,
//     0.8333333333333334,
//     0.8333333333333334,
//     0.8333333333333334,
//     0.8333333333333334,
//     0.8333333333333334,
//     0.8333333333333334
// ]

main();