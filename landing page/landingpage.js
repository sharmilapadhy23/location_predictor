var tl = gsap.timeline()

tl.from("h2",{
    y:-20,
    opacity: 0,
    duration: 0.5,
    delay:0.5
})

tl.from("h4",{
    y:-20,
    opacity: 0,
    duration: 0.3,
    delay:0.3,
    stagger: 0.3
})

var t2 = gsap.timeline()

t2.from(".para",{
    x:-20,
    opacity: 0,
    duration: 0.5,
    delay: 0.5
})

gsap.from(".image-sec",{
    x:20,
    opacity: 0,
    duration: 0.5,
    delay: 0.5
})



