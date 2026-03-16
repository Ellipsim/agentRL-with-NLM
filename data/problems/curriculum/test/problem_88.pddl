

(define (problem BW-rand-11)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 - block)
(:init
(handempty)
(ontable b1)
(ontable b2)
(on b3 b8)
(on b4 b9)
(on b5 b2)
(ontable b6)
(on b7 b6)
(on b8 b10)
(on b9 b5)
(on b10 b11)
(on b11 b7)
(clear b1)
(clear b3)
(clear b4)
)
(:goal
(and
(on b1 b4)
(on b2 b1)
(on b3 b9)
(on b6 b2)
(on b7 b8)
(on b8 b10)
(on b9 b5)
(on b10 b6)
(on b11 b3))
)
)


