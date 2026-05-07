

(define (problem BW-rand-12)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 - block)
(:init
(handempty)
(on b1 b2)
(on b2 b6)
(on b3 b10)
(on b4 b8)
(on b5 b3)
(on b6 b4)
(on b7 b12)
(on b8 b11)
(on b9 b1)
(on b10 b9)
(on b11 b7)
(ontable b12)
(clear b5)
)
(:goal
(and
(on b4 b5)
(on b5 b6)
(on b8 b11)
(on b9 b2)
(on b10 b9)
(on b11 b12)
(on b12 b10))
)
)


