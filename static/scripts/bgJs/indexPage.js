
import util from  './util.js'
import curvejs from  './index.js'

const  { Stage, Word, motion } = curvejs

var lineCount = 10,
    random = util.random,
    randomColor = util.randomColor,
    randomSpeed = util.randomSpeed,
    stage = new Stage(800,450,'#container')

function generatePosition(){

    stage.add(new Word('s',{
        color: '#22CAB3',
        motion: motion.dance,
        data: {angle: 0, r:5 ,step:Math.PI / 50 }

    }))


    stage.add(new Word('p',{
        color: '#22CAB3',
        x:60,
        motion: motion.dance,
        data: {angle: 0, r:5 ,step:Math.PI / 50 }
    }))

    stage.add(new Word('i',{
        color: '#22CAB3',
        x:145,
        motion: motion.dance,
        data: {angle: 0, r:5 ,step:Math.PI / 50 }
    }))

    stage.add(new Word('d',{
        color: '#22CAB3',
        x:210,
        y:10,
        motion: motion.dance,
        data: {angle: 0, r:5 ,step:Math.PI / 50 }
    }))

    stage.add(new Word('e',{
        color: '#22CAB3',
        x:280,
        y:-5,
        motion: motion.dance,
        data: {angle: 0, r:5 ,step:Math.PI / 50 }
    }))

    stage.add(new Word('r',{
        color: '#FF7784',
        x:350,
        motion: motion.dance,
        data: {angle: 0, r:5 ,step:Math.PI / 50 }
    }))

    stage.add(new Word('b',{
        color: '#FF7784',
        x:400,
        motion: motion.dance,
        data: {angle: 0, r:5 ,step:Math.PI / 50 }
    }))
}


function tick(){
    stage.update()
    requestAnimationFrame(tick)
}

;(function main(){
    generatePosition()
    tick()
})()