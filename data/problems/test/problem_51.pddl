

(define (problem BW-rand-12)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 - block)
(:init
(handempty)
(on b1 b10)
(on b2 b1)
(on b3 b2)
(ontable b4)
(on b5 b12)
(on b6 b8)
(on b7 b6)
(on b8 b4)
(ontable b9)
(ontable b10)
(on b11 b7)
(on b12 b3)
(clear b5)
(clear b9)
(clear b11)
)
(:goal
(and
(on b1 b4)
(on b2 b8)
(on b3 b1)
(on b4 b7)
(on b5 b9)
(on b6 b10)
(on b7 b2)
(on b8 b11)
(on b9 b3)
(on b10 b12))
)
)


