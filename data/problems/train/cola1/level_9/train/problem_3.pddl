

(define (problem BW-rand-11)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 - block)
(:init
(handempty)
(ontable b1)
(on b2 b10)
(on b3 b2)
(on b4 b8)
(on b5 b7)
(on b6 b4)
(ontable b7)
(on b8 b1)
(on b9 b3)
(on b10 b11)
(on b11 b6)
(clear b5)
(clear b9)
)
(:goal
(and
(on b2 b1)
(on b3 b7)
(on b5 b9)
(on b7 b8)
(on b8 b2)
(on b9 b6)
(on b10 b4))
)
)


