

(define (problem BW-rand-11)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 - block)
(:init
(handempty)
(on b1 b10)
(on b2 b3)
(on b3 b4)
(on b4 b5)
(on b5 b7)
(ontable b6)
(on b7 b8)
(on b8 b9)
(on b9 b11)
(ontable b10)
(on b11 b6)
(clear b1)
(clear b2)
)
(:goal
(and
(on b1 b9)
(on b2 b8)
(on b3 b7)
(on b4 b10)
(on b9 b3))
)
)


