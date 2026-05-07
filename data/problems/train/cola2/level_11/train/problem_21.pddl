

(define (problem BW-rand-12)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 - block)
(:init
(handempty)
(on b1 b11)
(on b2 b5)
(on b3 b10)
(on b4 b12)
(ontable b5)
(ontable b6)
(on b7 b8)
(on b8 b3)
(on b9 b2)
(on b10 b9)
(on b11 b6)
(ontable b12)
(clear b1)
(clear b4)
(clear b7)
)
(:goal
(and
(on b1 b9)
(on b2 b11)
(on b3 b7)
(on b4 b1)
(on b6 b8)
(on b7 b12)
(on b9 b3))
)
)


