

(define (problem BW-rand-12)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 - block)
(:init
(handempty)
(on b1 b6)
(on b2 b5)
(ontable b3)
(ontable b4)
(on b5 b9)
(on b6 b12)
(ontable b7)
(on b8 b11)
(on b9 b8)
(on b10 b3)
(on b11 b10)
(ontable b12)
(clear b1)
(clear b2)
(clear b4)
(clear b7)
)
(:goal
(and
(on b1 b6)
(on b2 b1)
(on b3 b7)
(on b6 b9)
(on b8 b5)
(on b9 b10)
(on b10 b4)
(on b12 b2))
)
)


