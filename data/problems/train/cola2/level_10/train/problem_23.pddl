

(define (problem BW-rand-11)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 - block)
(:init
(handempty)
(on b1 b6)
(on b2 b7)
(ontable b3)
(on b4 b8)
(on b5 b9)
(ontable b6)
(on b7 b3)
(ontable b8)
(on b9 b11)
(on b10 b2)
(on b11 b10)
(clear b1)
(clear b4)
(clear b5)
)
(:goal
(and
(on b1 b9)
(on b2 b7)
(on b3 b11)
(on b4 b2)
(on b5 b6)
(on b6 b4)
(on b8 b5)
(on b10 b1)
(on b11 b8))
)
)


