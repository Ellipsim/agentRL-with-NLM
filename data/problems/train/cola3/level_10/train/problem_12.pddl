

(define (problem BW-rand-12)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 - block)
(:init
(handempty)
(on b1 b9)
(on b2 b10)
(on b3 b12)
(on b4 b8)
(on b5 b11)
(ontable b6)
(on b7 b3)
(on b8 b5)
(ontable b9)
(on b10 b1)
(on b11 b6)
(on b12 b2)
(clear b4)
(clear b7)
)
(:goal
(and
(on b1 b9)
(on b3 b7)
(on b4 b6)
(on b6 b3)
(on b7 b12)
(on b8 b4)
(on b9 b8)
(on b10 b5)
(on b11 b1)
(on b12 b10))
)
)


