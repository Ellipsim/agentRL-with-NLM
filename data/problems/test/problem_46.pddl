

(define (problem BW-rand-12)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 - block)
(:init
(handempty)
(ontable b1)
(on b2 b12)
(on b3 b5)
(on b4 b10)
(on b5 b2)
(on b6 b11)
(on b7 b9)
(on b8 b4)
(on b9 b6)
(on b10 b1)
(ontable b11)
(ontable b12)
(clear b3)
(clear b7)
(clear b8)
)
(:goal
(and
(on b1 b6)
(on b2 b12)
(on b4 b3)
(on b5 b1)
(on b6 b8)
(on b7 b11)
(on b8 b9)
(on b9 b4)
(on b10 b2))
)
)


