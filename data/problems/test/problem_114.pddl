

(define (problem BW-rand-12)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 - block)
(:init
(handempty)
(ontable b1)
(on b2 b9)
(ontable b3)
(on b4 b11)
(on b5 b10)
(ontable b6)
(on b7 b2)
(on b8 b7)
(on b9 b12)
(on b10 b4)
(ontable b11)
(on b12 b1)
(clear b3)
(clear b5)
(clear b6)
(clear b8)
)
(:goal
(and
(on b1 b9)
(on b2 b3)
(on b5 b8)
(on b7 b11)
(on b8 b7)
(on b9 b10)
(on b11 b6)
(on b12 b2))
)
)


