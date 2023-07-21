class Matek {
    static fokba(radian){
        return 180*radian/Math.PI;
    }

    static radianba(fokmertek){
        return Math.PI/radian*180;
    }

    static sin(x){
        return Math.sin(x);
    }

    static cos(x){
        return Math.cos(x);
    }

    static asin(x){
        return Matek.fokba(Math.asin(x));
    }

    static acos(x){
        return Matek.fokba(Math.acos(x));
    }

    static atg(x){
        return Matek.fokba(Math.atan(x));
    }
    
    static atg2(x, y){
        return Matek.fokba(Math.atan2(x,y));
    }
    
}
