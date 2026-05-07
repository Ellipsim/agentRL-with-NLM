

(define (problem BW-rand-12)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 - block)
(:init
(handempty)
(ontable b1)
(on b2 b10)
(on b3 b2)
(on b4 b6)
(on b5 b12)
(on b6 b3)
(on b7 b1)
(on b8 b4)
(ontable b9)
(on b10 b9)
(on b11 b8)
(on b12 b7)
(clear b5)
(clear b11)
)
(:goal
(and
(on b1 b2)
(on b3 b1)
(on b5 b4)
(on b6 b5)
(on b8 b12)
(on b9 b11)
(on b10 b8)
(on b11 b7))
)
)


