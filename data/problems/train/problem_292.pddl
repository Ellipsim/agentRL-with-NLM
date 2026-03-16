

(define (problem BW-rand-12)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 - block)
(:init
(handempty)
(on b1 b9)
(on b2 b7)
(ontable b3)
(on b4 b11)
(on b5 b4)
(on b6 b8)
(on b7 b5)
(ontable b8)
(on b9 b10)
(on b10 b6)
(on b11 b12)
(on b12 b3)
(clear b1)
(clear b2)
)
(:goal
(and
(on b1 b4)
(on b3 b9)
(on b4 b10)
(on b5 b7)
(on b7 b3)
(on b8 b12)
(on b9 b6)
(on b10 b8)
(on b12 b5))
)
)


