

(define (problem BW-rand-13)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 b13 - block)
(:init
(handempty)
(on b1 b12)
(on b2 b13)
(ontable b3)
(on b4 b5)
(ontable b5)
(ontable b6)
(on b7 b9)
(on b8 b11)
(on b9 b4)
(on b10 b7)
(on b11 b10)
(on b12 b6)
(ontable b13)
(clear b1)
(clear b2)
(clear b3)
(clear b8)
)
(:goal
(and
(on b1 b6)
(on b4 b11)
(on b5 b13)
(on b6 b2)
(on b8 b3)
(on b9 b5)
(on b11 b8)
(on b12 b10))
)
)


