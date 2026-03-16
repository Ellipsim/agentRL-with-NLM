

(define (problem BW-rand-12)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 - block)
(:init
(handempty)
(on b1 b11)
(on b2 b7)
(on b3 b9)
(on b4 b1)
(on b5 b10)
(on b6 b3)
(ontable b7)
(on b8 b5)
(on b9 b4)
(on b10 b12)
(ontable b11)
(on b12 b6)
(clear b2)
(clear b8)
)
(:goal
(and
(on b1 b6)
(on b3 b11)
(on b4 b1)
(on b6 b2)
(on b7 b10)
(on b8 b9)
(on b11 b8)
(on b12 b5))
)
)


