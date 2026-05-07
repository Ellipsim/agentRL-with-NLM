

(define (problem BW-rand-12)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 - block)
(:init
(handempty)
(on b1 b9)
(ontable b2)
(on b3 b7)
(on b4 b2)
(on b5 b4)
(ontable b6)
(on b7 b11)
(on b8 b12)
(on b9 b10)
(on b10 b5)
(on b11 b1)
(on b12 b6)
(clear b3)
(clear b8)
)
(:goal
(and
(on b3 b4)
(on b4 b8)
(on b5 b11)
(on b6 b3)
(on b7 b2)
(on b9 b1)
(on b10 b6)
(on b11 b12)
(on b12 b10))
)
)


