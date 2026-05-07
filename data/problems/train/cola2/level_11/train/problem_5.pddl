

(define (problem BW-rand-13)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 b13 - block)
(:init
(handempty)
(on b1 b9)
(on b2 b3)
(on b3 b5)
(ontable b4)
(on b5 b7)
(ontable b6)
(on b7 b8)
(on b8 b13)
(on b9 b6)
(ontable b10)
(ontable b11)
(on b12 b2)
(ontable b13)
(clear b1)
(clear b4)
(clear b10)
(clear b11)
(clear b12)
)
(:goal
(and
(on b1 b13)
(on b2 b3)
(on b3 b9)
(on b5 b6)
(on b9 b8)
(on b10 b12)
(on b11 b4))
)
)


