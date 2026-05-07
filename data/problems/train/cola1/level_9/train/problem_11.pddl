

(define (problem BW-rand-11)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 - block)
(:init
(handempty)
(on b1 b8)
(on b2 b9)
(on b3 b7)
(on b4 b11)
(ontable b5)
(on b6 b2)
(on b7 b6)
(ontable b8)
(on b9 b10)
(on b10 b1)
(on b11 b5)
(clear b3)
(clear b4)
)
(:goal
(and
(on b1 b11)
(on b3 b9)
(on b4 b3)
(on b5 b1)
(on b7 b2)
(on b8 b7)
(on b10 b6)
(on b11 b8))
)
)


