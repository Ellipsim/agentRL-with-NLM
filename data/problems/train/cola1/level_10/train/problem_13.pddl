

(define (problem BW-rand-12)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 - block)
(:init
(handempty)
(on b1 b4)
(on b2 b1)
(on b3 b10)
(on b4 b9)
(on b5 b11)
(on b6 b3)
(ontable b7)
(on b8 b6)
(ontable b9)
(on b10 b7)
(on b11 b2)
(ontable b12)
(clear b5)
(clear b8)
(clear b12)
)
(:goal
(and
(on b1 b12)
(on b2 b7)
(on b3 b9)
(on b4 b3)
(on b5 b4)
(on b7 b8)
(on b8 b10)
(on b9 b11)
(on b10 b1)
(on b11 b2))
)
)


