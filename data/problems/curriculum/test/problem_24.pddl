

(define (problem BW-rand-12)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 - block)
(:init
(handempty)
(on b1 b12)
(ontable b2)
(on b3 b4)
(on b4 b9)
(ontable b5)
(on b6 b5)
(on b7 b1)
(on b8 b3)
(ontable b9)
(on b10 b2)
(on b11 b6)
(ontable b12)
(clear b7)
(clear b8)
(clear b10)
(clear b11)
)
(:goal
(and
(on b1 b2)
(on b3 b6)
(on b5 b3)
(on b6 b10)
(on b7 b8)
(on b9 b7)
(on b10 b11)
(on b11 b12))
)
)


