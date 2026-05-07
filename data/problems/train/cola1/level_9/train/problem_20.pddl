

(define (problem BW-rand-11)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 - block)
(:init
(handempty)
(on b1 b9)
(on b2 b8)
(on b3 b6)
(ontable b4)
(on b5 b11)
(on b6 b1)
(on b7 b10)
(ontable b8)
(ontable b9)
(on b10 b5)
(on b11 b3)
(clear b2)
(clear b4)
(clear b7)
)
(:goal
(and
(on b1 b11)
(on b2 b5)
(on b3 b4)
(on b4 b2)
(on b6 b9)
(on b7 b6)
(on b8 b7)
(on b9 b3)
(on b10 b1)
(on b11 b8))
)
)


