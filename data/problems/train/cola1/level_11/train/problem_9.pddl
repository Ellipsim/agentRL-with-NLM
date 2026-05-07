

(define (problem BW-rand-13)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 b13 - block)
(:init
(handempty)
(ontable b1)
(on b2 b4)
(on b3 b2)
(on b4 b1)
(on b5 b3)
(ontable b6)
(on b7 b10)
(ontable b8)
(on b9 b6)
(on b10 b12)
(on b11 b8)
(ontable b12)
(on b13 b7)
(clear b5)
(clear b9)
(clear b11)
(clear b13)
)
(:goal
(and
(on b1 b10)
(on b2 b7)
(on b5 b11)
(on b6 b1)
(on b8 b2)
(on b9 b3)
(on b12 b4)
(on b13 b8))
)
)


