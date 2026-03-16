

(define (problem BW-rand-12)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 - block)
(:init
(handempty)
(on b1 b10)
(on b2 b6)
(on b3 b2)
(ontable b4)
(on b5 b1)
(on b6 b4)
(ontable b7)
(on b8 b5)
(on b9 b8)
(on b10 b3)
(on b11 b7)
(on b12 b11)
(clear b9)
(clear b12)
)
(:goal
(and
(on b1 b2)
(on b2 b9)
(on b3 b4)
(on b4 b10)
(on b8 b12)
(on b9 b3)
(on b10 b8)
(on b11 b1))
)
)


