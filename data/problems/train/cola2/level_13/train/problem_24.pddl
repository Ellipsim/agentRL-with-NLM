

(define (problem BW-rand-14)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 b13 b14 - block)
(:init
(handempty)
(on b1 b9)
(on b2 b7)
(ontable b3)
(on b4 b6)
(on b5 b8)
(on b6 b10)
(ontable b7)
(on b8 b3)
(on b9 b13)
(on b10 b12)
(on b11 b14)
(on b12 b1)
(ontable b13)
(on b14 b5)
(clear b2)
(clear b4)
(clear b11)
)
(:goal
(and
(on b2 b13)
(on b4 b14)
(on b5 b10)
(on b6 b7)
(on b7 b5)
(on b9 b1)
(on b10 b12)
(on b11 b2))
)
)


