

(define (problem BW-rand-12)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 - block)
(:init
(handempty)
(ontable b1)
(on b2 b11)
(on b3 b10)
(on b4 b6)
(on b5 b9)
(on b6 b2)
(ontable b7)
(on b8 b1)
(on b9 b12)
(on b10 b7)
(on b11 b5)
(ontable b12)
(clear b3)
(clear b4)
(clear b8)
)
(:goal
(and
(on b2 b4)
(on b3 b9)
(on b4 b6)
(on b6 b11)
(on b8 b7)
(on b10 b5)
(on b11 b8)
(on b12 b2))
)
)


