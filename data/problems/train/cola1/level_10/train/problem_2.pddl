

(define (problem BW-rand-12)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 - block)
(:init
(handempty)
(ontable b1)
(on b2 b9)
(on b3 b1)
(on b4 b2)
(on b5 b4)
(ontable b6)
(on b7 b3)
(on b8 b7)
(on b9 b8)
(on b10 b11)
(on b11 b12)
(on b12 b6)
(clear b5)
(clear b10)
)
(:goal
(and
(on b1 b12)
(on b2 b11)
(on b3 b9)
(on b5 b10)
(on b7 b8)
(on b9 b1)
(on b11 b4)
(on b12 b7))
)
)


