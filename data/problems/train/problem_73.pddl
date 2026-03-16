

(define (problem BW-rand-12)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 - block)
(:init
(handempty)
(on b1 b11)
(on b2 b10)
(ontable b3)
(on b4 b3)
(on b5 b9)
(on b6 b12)
(on b7 b2)
(on b8 b4)
(on b9 b7)
(ontable b10)
(ontable b11)
(on b12 b8)
(clear b1)
(clear b5)
(clear b6)
)
(:goal
(and
(on b1 b3)
(on b3 b5)
(on b4 b1)
(on b6 b7)
(on b7 b9)
(on b8 b6)
(on b9 b12)
(on b11 b10)
(on b12 b11))
)
)


